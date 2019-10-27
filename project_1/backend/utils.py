import re
import datetime

_OPERATOR_SYMBOLS = {
    'or': ' | ',
    'and': ' & ',
}


def get_database_ref():
    import psycopg2
    database_connection = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="db",
        port="5432"
    )
    return database_connection, database_connection.cursor()


def parse_search_query(query, logical_op):
    logical_op_symbol = _OPERATOR_SYMBOLS[logical_op]

    quoted_parts = re.findall(pattern='\"(.+?)\"', string=query)

    query = query.replace('"', '')
    for quoted_part in quoted_parts:
        query = query.replace(quoted_part, '')

    query_parts = query.strip().split() + quoted_parts

    query = logical_op_symbol.join(
        '(' + _OPERATOR_SYMBOLS['and'].join(part.split()) + ')'
        for part in query_parts
    )

    return query, query_parts


def build_search_query(raw_query, logical_op):
    query, query_parts = parse_search_query(raw_query, logical_op)

    full_query = ""
    full_query += "SELECT"
    full_query += "\n  movieid,"
    full_query += f"\n  ts_headline(title, to_tsquery('english', '{query}')),"
    full_query += f"\n  ts_headline(description, to_tsquery('english', '{query}')),"
    full_query += f"\n  description,"
    full_query += f"\n  ts_rank(allAboutMovieTSVm, to_tsquery('english', '{query}'), 2) rank"
    full_query += f"\nFROM movie"
    full_query += f"\nWHERE"
    full_query += f"\n {logical_op.upper()} ".join(
        f"\n allAboutMovieTSVm @@ to_tsquery('english', '{' & '.join(query_part.split())}')"
        for query_part in query_parts
    )
    full_query += f"\nORDER BY rank DESC"

    return full_query


def build_analysis_query(start_date, end_date, granulation):
    if granulation == 'hours':
        return f"""
                SELECT *
                FROM crosstab(
                    'SELECT 
                        CAST(query as VARCHAR(255)) as query, 
                        EXTRACT(HOUR FROM queryTimestamp)::INT AS queryHour,
                        COUNT(*)::INT AS queryCount
                    FROM query_logging
                    WHERE queryTimestamp > (''{start_date}'')::TIMESTAMP AND queryTimestamp < (''{end_date}'')::TIMESTAMP
                    GROUP BY query, queryHour
                    ORDER BY query, queryHour'
                    ,
                    'SELECT CAST(queryHour AS INT) FROM queryHour ORDER BY queryHour' 
                )
                AS hourTable (
                    query VARCHAR(255),
                    s00_01 INT, s01_02 INT, s02_03 INT, s03_04 INT, s04_05 INT, s05_06 INT,
                    s06_07 INT, s07_08 INT, s08_09 INT, s09_10 INT, s10_11 INT, s11_12 INT,
                    s12_13 INT, s13_14 INT, s14_15 INT, s15_16 INT, s16_17 INT, s17_18 INT,
                    s18_19 INT, s19_20 INT, s20_21 INT, s21_22 INT, s22_23 INT, s23_00 INT
                )
                ORDER BY query;
                """
    else:
        from dateutil.parser import parse
        days_between = abs((parse(end_date) - parse(start_date)).days) + 1

        return f"""
                SELECT *
                FROM crosstab(
                    'SELECT 
                        CAST(query as VARCHAR(255)) as query,
                        queryTimestamp::DATE AS queryDay,
                        COUNT(*)::INT AS queryCount
                    FROM query_logging
                    WHERE queryTimestamp > (''{start_date}'')::TIMESTAMP AND queryTimestamp < (''{end_date}'')::TIMESTAMP
                    GROUP BY query, queryDay
                    ORDER BY query, queryDay'
                    ,
                    'SELECT day::DATE
                    FROM generate_series(
                        timestamp without time zone ''{start_date}'',
                        timestamp without time zone ''{end_date}'',
                        ''1 day''
                    )
                    as date_range(day)'
                )
                AS hourTable (
                    query VARCHAR(255),
                    {
                        ", ".join(
                            f"d{str((parse(start_date) + datetime.timedelta(days=i)).date()).replace('-', '')} INT"
                            for i in range(days_between)
                        )
                    }
                )
                ORDER BY query;
                """
