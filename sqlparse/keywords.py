# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2018 the sqlparse authors and contributors
# <see AUTHORS file>
#
# This module is part of python-sqlparse and is released under
# the BSD License: https://opensource.org/licenses/BSD-3-Clause

import re

from sqlparse import tokens

DB = "BIGQUERY"


def is_keyword(value):
    val = value.upper()
    if DB == "BIGQUERY":
        return (KEYWORDS_COMMON.get(val) or
                KEYWORDS_CTE.get(val) or 
                KEYWORDS_BIGQUERY_BUILTIN.get(val) or
                KEYWORDS_BIGQUERY_FUNCTIONS.get(val) or
                KEYWORDS_BIGQUERY.get(val, tokens.Name)), value

    else:
        return (KEYWORDS_COMMON.get(val) or
                KEYWORDS_CTE.get(val) or
                KEYWORDS_ORACLE.get(val) or
                KEYWORDS_PLPGSQL.get(val) or
                KEYWORDS.get(val, tokens.Name)), value


SQL_REGEX = {
    'root': [
        (r'(--|# )\+.*?(\r\n|\r|\n|$)', tokens.Comment.Single.Hint),
        (r'/\*\+[\s\S]*?\*/', tokens.Comment.Multiline.Hint),

        (r'(--|# ).*?(\r\n|\r|\n|$)', tokens.Comment.Single),
        (r'/\*[\s\S]*?\*/', tokens.Comment.Multiline),

        (r'(\r\n|\r|\n)', tokens.Newline),
        (r'\s+?', tokens.Whitespace),

        (r':=', tokens.Assignment),
        (r'::', tokens.Punctuation),

        (r'\*', tokens.Wildcard),

        (r"`(``|[^`])*`", tokens.Name),
        (r"´(´´|[^´])*´", tokens.Name),
        (r'(\$(?:[_A-ZÀ-Ü]\w*)?\$)[\s\S]*?\1', tokens.Literal),

        (r'\?', tokens.Name.Placeholder),
        (r'%(\(\w+\))?s', tokens.Name.Placeholder),
        (r'(?<!\w)[$:?]\w+', tokens.Name.Placeholder),

        # FIXME(andi): VALUES shouldn't be listed here
        # see https://github.com/andialbrecht/sqlparse/pull/64
        # IN is special, it may be followed by a parenthesis, but
        # is never a function, see issue183
        (r'(CASE|IN|VALUES|USING|FROM)\b', tokens.Keyword),

        (r'(@|##|#)[A-ZÀ-Ü]\w+', tokens.Name),

        # see issue #39
        # Spaces around period `schema . name` are valid identifier
        # TODO: Spaces before period not implemented
        (r'[A-ZÀ-Ü]\w*(?=\s*\.)', tokens.Name),  # 'Name'   .
        # FIXME(atronah): never match,
        # because `re.match` doesn't work with look-behind regexp feature
        (r'(?<=\.)[A-ZÀ-Ü]\w*', tokens.Name),  # .'Name'
        (r'[A-ZÀ-Ü]\w*(?=\()', tokens.Name),  # side effect: change kw to func
        (r'-?0x[\dA-F]+', tokens.Number.Hexadecimal),
        (r'-?\d*(\.\d+)?E-?\d+', tokens.Number.Float),
        (r'-?(\d+(\.\d*)|\.\d+)', tokens.Number.Float),
        (r'-?\d+(?![_A-ZÀ-Ü])', tokens.Number.Integer),
        (r"'(''|\\\\|\\'|[^'])*'", tokens.String.Single),
        # not a real string literal in ANSI SQL:
        (r'"(""|\\\\|\\"|[^"])*"', tokens.String.Symbol),
        (r'(""|".*?[^\\]")', tokens.String.Symbol),
        # sqlite names can be escaped with [square brackets]. left bracket
        # cannot be preceded by word character or a right bracket --
        # otherwise it's probably an array index
        (r'(?<![\w\])])(\[[^\]]+\])', tokens.Name),
        (r'((LEFT\s+|RIGHT\s+|FULL\s+)?(INNER\s+|OUTER\s+|STRAIGHT\s+)?'
         r'|(CROSS\s+|NATURAL\s+)?)?JOIN\b', tokens.Keyword),
        (r'END(\s+IF|\s+LOOP|\s+WHILE)?\b', tokens.Keyword),
        (r'NOT\s+NULL\b', tokens.Keyword),
        (r'UNION\s+ALL\b', tokens.Keyword),
        (r'CREATE(\s+OR\s+REPLACE)?\b', tokens.Keyword.DDL),
        (r'DOUBLE\s+PRECISION\b', tokens.Name.Builtin),

        (r'[0-9_A-ZÀ-Ü][_$#\w]*', is_keyword),

        (r'[;:()\[\],\.]', tokens.Punctuation),
        (r'[<>=~!]+', tokens.Operator.Comparison),
        (r'[+/@#%^&|`?^-]+', tokens.Operator),
    ]}

FLAGS = re.IGNORECASE | re.UNICODE
SQL_REGEX = [(re.compile(rx, FLAGS).match, tt) for rx, tt in SQL_REGEX['root']]
KEYWORDS = {
    'ABORT': tokens.Keyword,
    'ABS': tokens.Keyword,
    'ABSOLUTE': tokens.Keyword,
    'ACCESS': tokens.Keyword,
    'ADA': tokens.Keyword,
    'ADD': tokens.Keyword,
    'ADMIN': tokens.Keyword,
    'AFTER': tokens.Keyword,
    'AGGREGATE': tokens.Keyword,
    'ALIAS': tokens.Keyword,
    'ALL': tokens.Keyword,
    'ALLOCATE': tokens.Keyword,
    'ANALYSE': tokens.Keyword,
    'ANALYZE': tokens.Keyword,
    'ANY': tokens.Keyword,
    'ARRAYLEN': tokens.Keyword,
    'ARE': tokens.Keyword,
    'ASC': tokens.Keyword.Order,
    'ASENSITIVE': tokens.Keyword,
    'ASSERTION': tokens.Keyword,
    'ASSIGNMENT': tokens.Keyword,
    'ASYMMETRIC': tokens.Keyword,
    'AT': tokens.Keyword,
    'ATOMIC': tokens.Keyword,
    'AS': tokens.Keyword,
    'AUDIT': tokens.Keyword,
    'AUTHORIZATION': tokens.Keyword,
    'AUTO_INCREMENT': tokens.Keyword,
    'AVG': tokens.Keyword,

    'BACKWARD': tokens.Keyword,
    'BEFORE': tokens.Keyword,
    'BEGIN': tokens.Keyword,
    'BETWEEN': tokens.Keyword,
    'BITVAR': tokens.Keyword,
    'BIT_LENGTH': tokens.Keyword,
    'BOTH': tokens.Keyword,
    'BREADTH': tokens.Keyword,

    # 'C': tokens.Keyword,  # most likely this is an alias
    'CACHE': tokens.Keyword,
    'CALL': tokens.Keyword,
    'CALLED': tokens.Keyword,
    'CARDINALITY': tokens.Keyword,
    'CASCADE': tokens.Keyword,
    'CASCADED': tokens.Keyword,
    'CAST': tokens.Keyword,
    'CATALOG': tokens.Keyword,
    'CATALOG_NAME': tokens.Keyword,
    'CHAIN': tokens.Keyword,
    'CHARACTERISTICS': tokens.Keyword,
    'CHARACTER_LENGTH': tokens.Keyword,
    'CHARACTER_SET_CATALOG': tokens.Keyword,
    'CHARACTER_SET_NAME': tokens.Keyword,
    'CHARACTER_SET_SCHEMA': tokens.Keyword,
    'CHAR_LENGTH': tokens.Keyword,
    'CHARSET': tokens.Keyword,
    'CHECK': tokens.Keyword,
    'CHECKED': tokens.Keyword,
    'CHECKPOINT': tokens.Keyword,
    'CLASS': tokens.Keyword,
    'CLASS_ORIGIN': tokens.Keyword,
    'CLOB': tokens.Keyword,
    'CLOSE': tokens.Keyword,
    'CLUSTER': tokens.Keyword,
    'COALESCE': tokens.Keyword,
    'COBOL': tokens.Keyword,
    'COLLATE': tokens.Keyword,
    'COLLATION': tokens.Keyword,
    'COLLATION_CATALOG': tokens.Keyword,
    'COLLATION_NAME': tokens.Keyword,
    'COLLATION_SCHEMA': tokens.Keyword,
    'COLLECT': tokens.Keyword,
    'COLUMN': tokens.Keyword,
    'COLUMN_NAME': tokens.Keyword,
    'COMPRESS': tokens.Keyword,
    'COMMAND_FUNCTION': tokens.Keyword,
    'COMMAND_FUNCTION_CODE': tokens.Keyword,
    'COMMENT': tokens.Keyword,
    'COMMIT': tokens.Keyword.DML,
    'COMMITTED': tokens.Keyword,
    'COMPLETION': tokens.Keyword,
    'CONCURRENTLY': tokens.Keyword,
    'CONDITION_NUMBER': tokens.Keyword,
    'CONNECT': tokens.Keyword,
    'CONNECTION': tokens.Keyword,
    'CONNECTION_NAME': tokens.Keyword,
    'CONSTRAINT': tokens.Keyword,
    'CONSTRAINTS': tokens.Keyword,
    'CONSTRAINT_CATALOG': tokens.Keyword,
    'CONSTRAINT_NAME': tokens.Keyword,
    'CONSTRAINT_SCHEMA': tokens.Keyword,
    'CONSTRUCTOR': tokens.Keyword,
    'CONTAINS': tokens.Keyword,
    'CONTINUE': tokens.Keyword,
    'CONVERSION': tokens.Keyword,
    'CONVERT': tokens.Keyword,
    'COPY': tokens.Keyword,
    'CORRESPONTING': tokens.Keyword,
    'COUNT': tokens.Keyword,
    'CREATEDB': tokens.Keyword,
    'CREATEUSER': tokens.Keyword,
    'CROSS': tokens.Keyword,
    'CUBE': tokens.Keyword,
    'CURRENT': tokens.Keyword,
    'CURRENT_DATE': tokens.Keyword,
    'CURRENT_PATH': tokens.Keyword,
    'CURRENT_ROLE': tokens.Keyword,
    'CURRENT_TIME': tokens.Keyword,
    'CURRENT_TIMESTAMP': tokens.Keyword,
    'CURRENT_USER': tokens.Keyword,
    'CURSOR': tokens.Keyword,
    'CURSOR_NAME': tokens.Keyword,
    'CYCLE': tokens.Keyword,

    'DATA': tokens.Keyword,
    'DATABASE': tokens.Keyword,
    'DATETIME_INTERVAL_CODE': tokens.Keyword,
    'DATETIME_INTERVAL_PRECISION': tokens.Keyword,
    'DAY': tokens.Keyword,
    'DEALLOCATE': tokens.Keyword,
    'DECLARE': tokens.Keyword,
    'DEFAULT': tokens.Keyword,
    'DEFAULTS': tokens.Keyword,
    'DEFERRABLE': tokens.Keyword,
    'DEFERRED': tokens.Keyword,
    'DEFINED': tokens.Keyword,
    'DEFINER': tokens.Keyword,
    'DELIMITER': tokens.Keyword,
    'DELIMITERS': tokens.Keyword,
    'DEREF': tokens.Keyword,
    'DESC': tokens.Keyword.Order,
    'DESCRIBE': tokens.Keyword,
    'DESCRIPTOR': tokens.Keyword,
    'DESTROY': tokens.Keyword,
    'DESTRUCTOR': tokens.Keyword,
    'DETERMINISTIC': tokens.Keyword,
    'DIAGNOSTICS': tokens.Keyword,
    'DICTIONARY': tokens.Keyword,
    'DISABLE': tokens.Keyword,
    'DISCONNECT': tokens.Keyword,
    'DISPATCH': tokens.Keyword,
    'DO': tokens.Keyword,
    'DOMAIN': tokens.Keyword,
    'DYNAMIC': tokens.Keyword,
    'DYNAMIC_FUNCTION': tokens.Keyword,
    'DYNAMIC_FUNCTION_CODE': tokens.Keyword,

    'EACH': tokens.Keyword,
    'ENABLE': tokens.Keyword,
    'ENCODING': tokens.Keyword,
    'ENCRYPTED': tokens.Keyword,
    'END-EXEC': tokens.Keyword,
    'ENGINE': tokens.Keyword,
    'EQUALS': tokens.Keyword,
    'ESCAPE': tokens.Keyword,
    'EVERY': tokens.Keyword,
    'EXCEPT': tokens.Keyword,
    'EXCEPTION': tokens.Keyword,
    'EXCLUDING': tokens.Keyword,
    'EXCLUSIVE': tokens.Keyword,
    'EXEC': tokens.Keyword,
    'EXECUTE': tokens.Keyword,
    'EXISTING': tokens.Keyword,
    'EXISTS': tokens.Keyword,
    'EXPLAIN': tokens.Keyword,
    'EXTERNAL': tokens.Keyword,
    'EXTRACT': tokens.Keyword,

    'FALSE': tokens.Keyword,
    'FETCH': tokens.Keyword,
    'FILE': tokens.Keyword,
    'FINAL': tokens.Keyword,
    'FIRST': tokens.Keyword,
    'FORCE': tokens.Keyword,
    'FOREACH': tokens.Keyword,
    'FOREIGN': tokens.Keyword,
    'FORTRAN': tokens.Keyword,
    'FORWARD': tokens.Keyword,
    'FOUND': tokens.Keyword,
    'FREE': tokens.Keyword,
    # 'FREEZE': tokens.Keyword,
    'FULL': tokens.Keyword,
    'FUNCTION': tokens.Keyword,

    # 'G': tokens.Keyword,
    'GENERAL': tokens.Keyword,
    'GENERATED': tokens.Keyword,
    'GET': tokens.Keyword,
    'GLOBAL': tokens.Keyword,
    'GO': tokens.Keyword,
    'GOTO': tokens.Keyword,
    'GRANT': tokens.Keyword,
    'GRANTED': tokens.Keyword,
    'GROUPING': tokens.Keyword,

    'HANDLER': tokens.Keyword,
    'HAVING': tokens.Keyword,
    'HIERARCHY': tokens.Keyword,
    'HOLD': tokens.Keyword,
    'HOST': tokens.Keyword,

    'IDENTIFIED': tokens.Keyword,
    'IDENTITY': tokens.Keyword,
    'IGNORE': tokens.Keyword,
    'ILIKE': tokens.Keyword,
    'IMMEDIATE': tokens.Keyword,
    'IMMUTABLE': tokens.Keyword,

    'IMPLEMENTATION': tokens.Keyword,
    'IMPLICIT': tokens.Keyword,
    'INCLUDING': tokens.Keyword,
    'INCREMENT': tokens.Keyword,
    'INDEX': tokens.Keyword,

    'INDITCATOR': tokens.Keyword,
    'INFIX': tokens.Keyword,
    'INHERITS': tokens.Keyword,
    'INITIAL': tokens.Keyword,
    'INITIALIZE': tokens.Keyword,
    'INITIALLY': tokens.Keyword,
    'INOUT': tokens.Keyword,
    'INPUT': tokens.Keyword,
    'INSENSITIVE': tokens.Keyword,
    'INSTANTIABLE': tokens.Keyword,
    'INSTEAD': tokens.Keyword,
    'INTERSECT': tokens.Keyword,
    'INTO': tokens.Keyword,
    'INVOKER': tokens.Keyword,
    'IS': tokens.Keyword,
    'ISNULL': tokens.Keyword,
    'ISOLATION': tokens.Keyword,
    'ITERATE': tokens.Keyword,

    # 'K': tokens.Keyword,
    'KEY': tokens.Keyword,
    'KEY_MEMBER': tokens.Keyword,
    'KEY_TYPE': tokens.Keyword,

    'LANCOMPILER': tokens.Keyword,
    'LANGUAGE': tokens.Keyword,
    'LARGE': tokens.Keyword,
    'LAST': tokens.Keyword,
    'LATERAL': tokens.Keyword,
    'LEADING': tokens.Keyword,
    'LENGTH': tokens.Keyword,
    'LESS': tokens.Keyword,
    'LEVEL': tokens.Keyword,
    'LIMIT': tokens.Keyword,
    'LISTEN': tokens.Keyword,
    'LOAD': tokens.Keyword,
    'LOCAL': tokens.Keyword,
    'LOCALTIME': tokens.Keyword,
    'LOCALTIMESTAMP': tokens.Keyword,
    'LOCATION': tokens.Keyword,
    'LOCATOR': tokens.Keyword,
    'LOCK': tokens.Keyword,
    'LOWER': tokens.Keyword,

    # 'M': tokens.Keyword,
    # 'MAP': tokens.Keyword,
    'MATCH': tokens.Keyword,
    'MAXEXTENTS': tokens.Keyword,
    'MAXVALUE': tokens.Keyword,
    'MESSAGE_LENGTH': tokens.Keyword,
    'MESSAGE_OCTET_LENGTH': tokens.Keyword,
    'MESSAGE_TEXT': tokens.Keyword,
    'METHOD': tokens.Keyword,
    'MINUTE': tokens.Keyword,
    'MINUS': tokens.Keyword,
    'MINVALUE': tokens.Keyword,
    'MOD': tokens.Keyword,
    'MODE': tokens.Keyword,
    'MODIFIES': tokens.Keyword,
    'MODIFY': tokens.Keyword,
    'MONTH': tokens.Keyword,
    'MORE': tokens.Keyword,
    'MOVE': tokens.Keyword,
    'MUMPS': tokens.Keyword,

    'NAMES': tokens.Keyword,
    'NATIONAL': tokens.Keyword,
    'NATURAL': tokens.Keyword,
    'NCHAR': tokens.Keyword,
    'NCLOB': tokens.Keyword,
    'NEW': tokens.Keyword,
    'NEXT': tokens.Keyword,
    'NO': tokens.Keyword,
    'NOAUDIT': tokens.Keyword,
    'NOCOMPRESS': tokens.Keyword,
    'NOCREATEDB': tokens.Keyword,
    'NOCREATEUSER': tokens.Keyword,
    'NONE': tokens.Keyword,
    'NOT': tokens.Keyword,
    'NOTFOUND': tokens.Keyword,
    'NOTHING': tokens.Keyword,
    'NOTIFY': tokens.Keyword,
    'NOTNULL': tokens.Keyword,
    'NOWAIT': tokens.Keyword,
    'NULL': tokens.Keyword,
    'NULLABLE': tokens.Keyword,
    'NULLIF': tokens.Keyword,

    'OBJECT': tokens.Keyword,
    'OCTET_LENGTH': tokens.Keyword,
    'OF': tokens.Keyword,
    'OFF': tokens.Keyword,
    'OFFLINE': tokens.Keyword,
    'OFFSET': tokens.Keyword,
    'OIDS': tokens.Keyword,
    'OLD': tokens.Keyword,
    'ONLINE': tokens.Keyword,
    'ONLY': tokens.Keyword,
    'OPEN': tokens.Keyword,
    'OPERATION': tokens.Keyword,
    'OPERATOR': tokens.Keyword,
    'OPTION': tokens.Keyword,
    'OPTIONS': tokens.Keyword,
    'ORDINALITY': tokens.Keyword,
    'OUT': tokens.Keyword,
    'OUTPUT': tokens.Keyword,
    'OVERLAPS': tokens.Keyword,
    'OVERLAY': tokens.Keyword,
    'OVERRIDING': tokens.Keyword,
    'OWNER': tokens.Keyword,

    'PAD': tokens.Keyword,
    'PARAMETER': tokens.Keyword,
    'PARAMETERS': tokens.Keyword,
    'PARAMETER_MODE': tokens.Keyword,
    'PARAMATER_NAME': tokens.Keyword,
    'PARAMATER_ORDINAL_POSITION': tokens.Keyword,
    'PARAMETER_SPECIFIC_CATALOG': tokens.Keyword,
    'PARAMETER_SPECIFIC_NAME': tokens.Keyword,
    'PARAMATER_SPECIFIC_SCHEMA': tokens.Keyword,
    'PARTIAL': tokens.Keyword,
    'PASCAL': tokens.Keyword,
    'PCTFREE': tokens.Keyword,
    'PENDANT': tokens.Keyword,
    'PLACING': tokens.Keyword,
    'PLI': tokens.Keyword,
    'POSITION': tokens.Keyword,
    'POSTFIX': tokens.Keyword,
    'PRECISION': tokens.Keyword,
    'PREFIX': tokens.Keyword,
    'PREORDER': tokens.Keyword,
    'PREPARE': tokens.Keyword,
    'PRESERVE': tokens.Keyword,
    'PRIMARY': tokens.Keyword,
    'PRIOR': tokens.Keyword,
    'PRIVILEGES': tokens.Keyword,
    'PROCEDURAL': tokens.Keyword,
    'PROCEDURE': tokens.Keyword,
    'PUBLIC': tokens.Keyword,

    'RAISE': tokens.Keyword,
    # 'RAW': tokens.Keyword,
    'READ': tokens.Keyword,
    'READS': tokens.Keyword,
    'RECHECK': tokens.Keyword,
    'RECURSIVE': tokens.Keyword,
    'REF': tokens.Keyword,
    'REFERENCES': tokens.Keyword,
    'REFERENCING': tokens.Keyword,
    'REINDEX': tokens.Keyword,
    'RELATIVE': tokens.Keyword,
    'RENAME': tokens.Keyword,
    'REPEATABLE': tokens.Keyword,
    'RESET': tokens.Keyword,
    'RESOURCE': tokens.Keyword,
    'RESTART': tokens.Keyword,
    'RESTRICT': tokens.Keyword,
    'RESULT': tokens.Keyword,
    'RETURN': tokens.Keyword,
    'RETURNED_LENGTH': tokens.Keyword,
    'RETURNED_OCTET_LENGTH': tokens.Keyword,
    'RETURNED_SQLSTATE': tokens.Keyword,
    'RETURNING': tokens.Keyword,
    'RETURNS': tokens.Keyword,
    'REVOKE': tokens.Keyword,
    'RIGHT': tokens.Keyword,
    'ROLE': tokens.Keyword,
    'ROLLBACK': tokens.Keyword.DML,
    'ROLLUP': tokens.Keyword,
    'ROUTINE': tokens.Keyword,
    'ROUTINE_CATALOG': tokens.Keyword,
    'ROUTINE_NAME': tokens.Keyword,
    'ROUTINE_SCHEMA': tokens.Keyword,
    'ROW': tokens.Keyword,
    'ROWS': tokens.Keyword,
    'ROW_COUNT': tokens.Keyword,
    'RULE': tokens.Keyword,

    'SAVE_POINT': tokens.Keyword,
    'SCALE': tokens.Keyword,
    'SCHEMA': tokens.Keyword,
    'SCHEMA_NAME': tokens.Keyword,
    'SCOPE': tokens.Keyword,
    'SCROLL': tokens.Keyword,
    'SEARCH': tokens.Keyword,
    'SECOND': tokens.Keyword,
    'SECURITY': tokens.Keyword,
    'SELF': tokens.Keyword,
    'SENSITIVE': tokens.Keyword,
    'SEQUENCE': tokens.Keyword,
    'SERIALIZABLE': tokens.Keyword,
    'SERVER_NAME': tokens.Keyword,
    'SESSION': tokens.Keyword,
    'SESSION_USER': tokens.Keyword,
    'SETOF': tokens.Keyword,
    'SETS': tokens.Keyword,
    'SHARE': tokens.Keyword,
    'SHOW': tokens.Keyword,
    'SIMILAR': tokens.Keyword,
    'SIMPLE': tokens.Keyword,
    'SIZE': tokens.Keyword,
    'SOME': tokens.Keyword,
    'SOURCE': tokens.Keyword,
    'SPACE': tokens.Keyword,
    'SPECIFIC': tokens.Keyword,
    'SPECIFICTYPE': tokens.Keyword,
    'SPECIFIC_NAME': tokens.Keyword,
    'SQL': tokens.Keyword,
    'SQLBUF': tokens.Keyword,
    'SQLCODE': tokens.Keyword,
    'SQLERROR': tokens.Keyword,
    'SQLEXCEPTION': tokens.Keyword,
    'SQLSTATE': tokens.Keyword,
    'SQLWARNING': tokens.Keyword,
    'STABLE': tokens.Keyword,
    'START': tokens.Keyword.DML,
    # 'STATE': tokens.Keyword,
    'STATEMENT': tokens.Keyword,
    'STATIC': tokens.Keyword,
    'STATISTICS': tokens.Keyword,
    'STDIN': tokens.Keyword,
    'STDOUT': tokens.Keyword,
    'STORAGE': tokens.Keyword,
    'STRICT': tokens.Keyword,
    'STRUCTURE': tokens.Keyword,
    'STYPE': tokens.Keyword,
    'SUBCLASS_ORIGIN': tokens.Keyword,
    'SUBLIST': tokens.Keyword,
    'SUBSTRING': tokens.Keyword,
    'SUCCESSFUL': tokens.Keyword,
    'SUM': tokens.Keyword,
    'SYMMETRIC': tokens.Keyword,
    'SYNONYM': tokens.Keyword,
    'SYSID': tokens.Keyword,
    'SYSTEM': tokens.Keyword,
    'SYSTEM_USER': tokens.Keyword,

    'TABLE': tokens.Keyword,
    'TABLE_NAME': tokens.Keyword,
    'TEMP': tokens.Keyword,
    'TEMPLATE': tokens.Keyword,
    'TEMPORARY': tokens.Keyword,
    'TERMINATE': tokens.Keyword,
    'THAN': tokens.Keyword,
    'TIMESTAMP': tokens.Keyword,
    'TIMEZONE_HOUR': tokens.Keyword,
    'TIMEZONE_MINUTE': tokens.Keyword,
    'TO': tokens.Keyword,
    'TOAST': tokens.Keyword,
    'TRAILING': tokens.Keyword,
    'TRANSATION': tokens.Keyword,
    'TRANSACTIONS_COMMITTED': tokens.Keyword,
    'TRANSACTIONS_ROLLED_BACK': tokens.Keyword,
    'TRANSATION_ACTIVE': tokens.Keyword,
    'TRANSFORM': tokens.Keyword,
    'TRANSFORMS': tokens.Keyword,
    'TRANSLATE': tokens.Keyword,
    'TRANSLATION': tokens.Keyword,
    'TREAT': tokens.Keyword,
    'TRIGGER': tokens.Keyword,
    'TRIGGER_CATALOG': tokens.Keyword,
    'TRIGGER_NAME': tokens.Keyword,
    'TRIGGER_SCHEMA': tokens.Keyword,
    'TRIM': tokens.Keyword,
    'TRUE': tokens.Keyword,
    'TRUNCATE': tokens.Keyword,
    'TRUSTED': tokens.Keyword,
    'TYPE': tokens.Keyword,

    'UID': tokens.Keyword,
    'UNCOMMITTED': tokens.Keyword,
    'UNDER': tokens.Keyword,
    'UNENCRYPTED': tokens.Keyword,
    'UNION': tokens.Keyword,
    'UNIQUE': tokens.Keyword,
    'UNKNOWN': tokens.Keyword,
    'UNLISTEN': tokens.Keyword,
    'UNNAMED': tokens.Keyword,
    'UNNEST': tokens.Keyword,
    'UNTIL': tokens.Keyword,
    'UPPER': tokens.Keyword,
    'USAGE': tokens.Keyword,
    'USE': tokens.Keyword,
    # 'USER': tokens.Keyword,
    'USER_DEFINED_TYPE_CATALOG': tokens.Keyword,
    'USER_DEFINED_TYPE_NAME': tokens.Keyword,
    'USER_DEFINED_TYPE_SCHEMA': tokens.Keyword,
    'USING': tokens.Keyword,

    'VACUUM': tokens.Keyword,
    'VALID': tokens.Keyword,
    'VALIDATE': tokens.Keyword,
    'VALIDATOR': tokens.Keyword,
    'VALUES': tokens.Keyword,
    'VARIABLE': tokens.Keyword,
    'VERBOSE': tokens.Keyword,
    'VERSION': tokens.Keyword,
    'VIEW': tokens.Keyword,
    'VOLATILE': tokens.Keyword,

    'WHENEVER': tokens.Keyword,
    'WITHOUT': tokens.Keyword,
    'WORK': tokens.Keyword,
    'WRITE': tokens.Keyword,

    'YEAR': tokens.Keyword,

    'ZONE': tokens.Keyword,

    # Name.Builtin
    'ARRAY': tokens.Name.Builtin,
    'BIGINT': tokens.Name.Builtin,
    'BINARY': tokens.Name.Builtin,
    'BIT': tokens.Name.Builtin,
    'BLOB': tokens.Name.Builtin,
    'BOOLEAN': tokens.Name.Builtin,
    'CHAR': tokens.Name.Builtin,
    'CHARACTER': tokens.Name.Builtin,
    'DATE': tokens.Name.Builtin,
    'DEC': tokens.Name.Builtin,
    'DECIMAL': tokens.Name.Builtin,
    'FLOAT': tokens.Name.Builtin,
    'INT': tokens.Name.Builtin,
    'INT8': tokens.Name.Builtin,
    'INTEGER': tokens.Name.Builtin,
    'INTERVAL': tokens.Name.Builtin,
    'LONG': tokens.Name.Builtin,
    'NUMBER': tokens.Name.Builtin,
    'NUMERIC': tokens.Name.Builtin,
    'REAL': tokens.Name.Builtin,
    'ROWID': tokens.Name.Builtin,
    'ROWLABEL': tokens.Name.Builtin,
    'ROWNUM': tokens.Name.Builtin,
    'SERIAL': tokens.Name.Builtin,
    'SERIAL8': tokens.Name.Builtin,
    'SIGNED': tokens.Name.Builtin,
    'SMALLINT': tokens.Name.Builtin,
    'SYSDATE': tokens.Name,
    'TEXT': tokens.Name.Builtin,
    'TINYINT': tokens.Name.Builtin,
    'UNSIGNED': tokens.Name.Builtin,
    'VARCHAR': tokens.Name.Builtin,
    'VARCHAR2': tokens.Name.Builtin,
    'VARYING': tokens.Name.Builtin,
}

KEYWORDS_CTE = {
    'WITH': tokens.Keyword.CTE,
}

KEYWORDS_COMMON = {
    'SELECT': tokens.Keyword.DML,
    'INSERT': tokens.Keyword.DML,
    'DELETE': tokens.Keyword.DML,
    'UPDATE': tokens.Keyword.DML,
    'UPSERT': tokens.Keyword.DML,
    'REPLACE': tokens.Keyword.DML,
    'MERGE': tokens.Keyword.DML,
    'DROP': tokens.Keyword.DDL,
    'CREATE': tokens.Keyword.DDL,
    'ALTER': tokens.Keyword.DDL,

    'WHERE': tokens.Keyword,
    'FROM': tokens.Keyword,
    'INNER': tokens.Keyword,
    'JOIN': tokens.Keyword,
    'STRAIGHT_JOIN': tokens.Keyword,
    'AND': tokens.Keyword,
    'OR': tokens.Keyword,
    'LIKE': tokens.Keyword,
    'ON': tokens.Keyword,
    'IN': tokens.Keyword,
    'SET': tokens.Keyword,

    'BY': tokens.Keyword,
    'GROUP': tokens.Keyword,
    'ORDER': tokens.Keyword,
    'LEFT': tokens.Keyword,
    'OUTER': tokens.Keyword,
    'FULL': tokens.Keyword,

    'IF': tokens.Keyword,
    'END': tokens.Keyword,
    'THEN': tokens.Keyword,
    'LOOP': tokens.Keyword,
    'AS': tokens.Keyword,
    'ELSE': tokens.Keyword,
    'FOR': tokens.Keyword,
    'WHILE': tokens.Keyword,

    'CASE': tokens.Keyword,
    'WHEN': tokens.Keyword,
    'MIN': tokens.Keyword,
    'MAX': tokens.Keyword,
    'DISTINCT': tokens.Keyword,
}

KEYWORDS_BIGQUERY = {
    'ALL': tokens.Keyword,
    'AND': tokens.Keyword,
    'ANY': tokens.Keyword,
    'ARRAY': tokens.Keyword,
    'AS': tokens.Keyword,
    'ASC': tokens.Keyword,
    'ASSERT_ROWS_MODIFIED': tokens.Keyword,
    'AT': tokens.Keyword,
    'BETWEEN': tokens.Keyword,
    'BY': tokens.Keyword,
    'CASE': tokens.Keyword,
    'CAST': tokens.Keyword,
    'COLLATE': tokens.Keyword,
    'CONTAINS': tokens.Keyword,
    'CROSS': tokens.Keyword,
    'CUBE': tokens.Keyword,
    'CURRENT': tokens.Keyword,
    'DEFAULT': tokens.Keyword,
    'DEFINE': tokens.Keyword,
    'DESC': tokens.Keyword,
    'DISTINCT': tokens.Keyword,
    'ELSE': tokens.Keyword,
    'END': tokens.Keyword,
    'ENUM': tokens.Keyword,
    'ESCAPE': tokens.Keyword,
    'EXCEPT': tokens.Keyword,
    'EXCLUDE': tokens.Keyword,
    'EXISTS': tokens.Keyword,
    'EXTRACT': tokens.Keyword,
    'FALSE': tokens.Keyword,
    'FETCH': tokens.Keyword,
    'FOLLOWING': tokens.Keyword,
    'FOR': tokens.Keyword,
    'FROM': tokens.Keyword,
    'FULL': tokens.Keyword,
    'GROUP': tokens.Keyword,
    'GROUPING': tokens.Keyword,
    'GROUPS': tokens.Keyword,
    'HASH': tokens.Keyword,
    'HAVING': tokens.Keyword,
    'IF': tokens.Keyword,
    'IGNORE': tokens.Keyword,
    'IN': tokens.Keyword,
    'INNER': tokens.Keyword,
    'INTERSECT': tokens.Keyword,
    'INTERVAL': tokens.Keyword,
    'INTO': tokens.Keyword,
    'IS': tokens.Keyword,
    'JOIN': tokens.Keyword,
    'LATERAL': tokens.Keyword,
    'LEFT': tokens.Keyword,
    'LIKE': tokens.Keyword,
    'LIMIT': tokens.Keyword,
    'LOOKUP': tokens.Keyword,
    'NATURAL': tokens.Keyword,
    'NEW': tokens.Keyword,
    'NO': tokens.Keyword,
    'NOT': tokens.Keyword,
    'NULL': tokens.Keyword,
    'NULLS': tokens.Keyword,
    'OF': tokens.Keyword,
    'ON': tokens.Keyword,
    'OR': tokens.Keyword,
    'ORDER': tokens.Keyword,
    'OUTER': tokens.Keyword,
    'OVER': tokens.Keyword,
    'PARTITION': tokens.Keyword,
    'PRECEDING': tokens.Keyword,
    'PROTO': tokens.Keyword,
    'RANGE': tokens.Keyword,
    'RECURSIVE': tokens.Keyword,
    'RESPECT': tokens.Keyword,
    'RIGHT': tokens.Keyword,
    'ROLLUP': tokens.Keyword,
    'ROWS': tokens.Keyword,
    'SAFE.': tokens.Keyword,
    'SET': tokens.Keyword,
    'SOME': tokens.Keyword,
    'STRUCT': tokens.Keyword,
    'TABLESAMPLE': tokens.Keyword,
    'THEN': tokens.Keyword,
    'TO': tokens.Keyword,
    'TREAT': tokens.Keyword,
    'TRUE': tokens.Keyword,
    'UNBOUNDED': tokens.Keyword,
    'UNION': tokens.Keyword,
    'UNNEST': tokens.Keyword,
    'USING': tokens.Keyword,
    'WHEN': tokens.Keyword,
    'WHERE': tokens.Keyword,
    'WINDOW': tokens.Keyword,
    'WITHIN': tokens.Keyword
}

KEYWORDS_BIGQUERY_BUILTIN = {
    'INT64': tokens.Name.Builtin,
    'NUMERIC': tokens.Name.Builtin,
    'FLOAT64': tokens.Name.Builtin,
    'BOOLEANSTRING': tokens.Name.Builtin,
    'BYTES': tokens.Name.Builtin,
    'DATE': tokens.Name.Builtin,
    'DATETIME': tokens.Name.Builtin,
    'GEOGRAPHY': tokens.Name.Builtin,
    'TIME': tokens.Name.Builtin,
    'TIMESTAMP': tokens.Name.Builtin,
    'ARRAY': tokens.Name.Builtin,
    'STRUCT': tokens.Name.Builtin,
}

KEYWORDS_BIGQUERY_FUNCTIONS = {
    'ANY_VALUE': tokens.Keyword,
    'ARAY_AGG': tokens.Keyword,
    'ARRAY_CONCAT_AGG': tokens.Keyword,
    'AVG': tokens.Keyword,
    'BIT_AND': tokens.Keyword,
    'BIT_OR': tokens.Keyword,
    'BIT_XOR': tokens.Keyword,
    'COUNT': tokens.Keyword,
    'COUNTIF': tokens.Keyword,
    'LOGICAL_AND': tokens.Keyword,
    'LOGICAL_OR': tokens.Keyword,
    'MAX': tokens.Keyword,
    'MIN': tokens.Keyword,
    'STRING_AGG': tokens.Keyword,
    'SUM': tokens.Keyword,
    'CORR': tokens.Keyword,
    'COVAR_POP': tokens.Keyword,
    'COVAR_SAMP': tokens.Keyword,
    'STDDEV_POP': tokens.Keyword,
    'STDDEV_SAMP': tokens.Keyword,
    'STDDEV': tokens.Keyword,
    'VAR_POP': tokens.Keyword,
    'VAR_SAMP': tokens.Keyword,
    'VARIANCE': tokens.Keyword,
    'APPROX_COUNT_DISTINCT': tokens.Keyword,
    'APPROX_QUANTILES': tokens.Keyword,
    'APPROX_TOP_COUNT': tokens.Keyword,
    'APPROX_TOP_SUM': tokens.Keyword,
    'HLL_COUNT.INIT': tokens.Keyword,
    'HLL_COUNT.MERGE': tokens.Keyword,
    'HLL_COUNT.MERGE_PARTIAL': tokens.Keyword,
    'HLL_COUNT.EXTRACT': tokens.Keyword,
    'RANK': tokens.Keyword,
    'DENSE_RANK': tokens.Keyword,
    'PERCENT_RANK': tokens.Keyword,
    'CUME_DIST': tokens.Keyword,
    'NTILE': tokens.Keyword,
    'ROW_NUMBER': tokens.Keyword,
    'BIT_COUNT': tokens.Keyword,
    'ABS': tokens.Keyword,
    'SIGN': tokens.Keyword,
    'IS_INF': tokens.Keyword,
    'IS_NAN': tokens.Keyword,
    'IEEE_DIVIDE': tokens.Keyword,
    'RAND': tokens.Keyword,
    'SQRT': tokens.Keyword,
    'POW': tokens.Keyword,
    'POWER': tokens.Keyword,
    'EXP': tokens.Keyword,
    'LN': tokens.Keyword,
    'LOG': tokens.Keyword,
    'LOG10': tokens.Keyword,
    'GREATEST': tokens.Keyword,
    'LEAST': tokens.Keyword,
    'DIV': tokens.Keyword,
    'SAFE_DIVIDE': tokens.Keyword,
    'MOD': tokens.Keyword,
    'ROUND': tokens.Keyword,
    'TRUNC': tokens.Keyword,
    'CEIL': tokens.Keyword,
    'CEILING': tokens.Keyword,
    'FLOOR': tokens.Keyword,
    'COS': tokens.Keyword,
    'COSH': tokens.Keyword,
    'ACOS': tokens.Keyword,
    'ACOSH': tokens.Keyword,
    'SIN': tokens.Keyword,
    'SINH': tokens.Keyword,
    'ASIN': tokens.Keyword,
    'ASINH': tokens.Keyword,
    'TAN': tokens.Keyword,
    'TANH': tokens.Keyword,
    'ATAN': tokens.Keyword,
    'ATANH': tokens.Keyword,
    'ATAN2': tokens.Keyword,
    'FIRST_VALUE ': tokens.Keyword,
    'LAST_VALUE ': tokens.Keyword,
    'NTH_VALUE ': tokens.Keyword,
    'LEAD ': tokens.Keyword,
    'LAG ': tokens.Keyword,
    'PERCENTILE_CONT ': tokens.Keyword,
    'PERCENTILE_DISC ': tokens.Keyword,
    'FARM_FINGERPRINT': tokens.Keyword,
    'MD5': tokens.Keyword,
    'SHA1': tokens.Keyword,
    'SHA256': tokens.Keyword,
    'SHA512': tokens.Keyword,
    'BYTE_LENGTH': tokens.Keyword,
    'CHAR_LENGTH': tokens.Keyword,
    'CHARACTER_LENGTH': tokens.Keyword,
    'CODE_POINTS_TO_BYTES': tokens.Keyword,
    'CODE_POINTS_TO_STRING': tokens.Keyword,
    'CONCAT': tokens.Keyword,
    'ENDS_WITH': tokens.Keyword,
    'FROM_BASE32': tokens.Keyword,
    'FROM_BASE64': tokens.Keyword,
    'FROM_HEX': tokens.Keyword,
    'LENGTH': tokens.Keyword,
    'LPAD': tokens.Keyword,
    'LOWER': tokens.Keyword,
    'LTRIM': tokens.Keyword,
    'NORMALIZE': tokens.Keyword,
    'NORMALIZE_AND_CASEFOLD': tokens.Keyword,
    'REGEXP_CONTAINS': tokens.Keyword,
    'REGEXP_EXTRACT': tokens.Keyword,
    'REGEXP_EXTRACT_ALL': tokens.Keyword,
    'REGEXP_REPLACE': tokens.Keyword,
    'REPLACE': tokens.Keyword,
    'REPEAT': tokens.Keyword,
    'REVERSE': tokens.Keyword,
    'RPAD': tokens.Keyword,
    'RTRIM': tokens.Keyword,
    'SAFE_CONVERT_BYTES_TO_STRING': tokens.Keyword,
    'SPLIT': tokens.Keyword,
    'STARTS_WITH': tokens.Keyword,
    'STRPOS': tokens.Keyword,
    'SUBSTR': tokens.Keyword,
    'TO_BASE32': tokens.Keyword,
    'TO_BASE64': tokens.Keyword,
    'TO_CODE_POINTS': tokens.Keyword,
    'TO_HEX': tokens.Keyword,
    'TRIM': tokens.Keyword,
    'UPPER': tokens.Keyword,
    'TO_JSON_STRING': tokens.Keyword,
    'ARRAY': tokens.Keyword,
    'ARRAY_CONCAT': tokens.Keyword,
    'ARRAY_LENGTH': tokens.Keyword,
    'ARRAY_TO_STRING': tokens.Keyword,
    'GENERATE_ARRAY': tokens.Keyword,
    'GENERATE_DATE_ARRAY': tokens.Keyword,
    'ARRAY_REVERSE': tokens.Keyword,
    'CURRENT_DATE': tokens.Keyword,
    'EXTRACT': tokens.Keyword,
    'DATE': tokens.Keyword,
    'DATE_ADD': tokens.Keyword,
    'DATE_SUB': tokens.Keyword,
    'DATE_DIFF': tokens.Keyword,
    'DATE_TRUNC': tokens.Keyword,
    'DATE_FROM_UNIX_DATE': tokens.Keyword,
    'FORMAT_DATE': tokens.Keyword,
    'PARSE_DATE': tokens.Keyword,
    'UNIX_DATE': tokens.Keyword,
    'CURRENT_DATETIME': tokens.Keyword,
    'DATETIME': tokens.Keyword,
    'DATETIME_ADD': tokens.Keyword,
    'DATETIME_SUB': tokens.Keyword,
    'DATETIME_DIFF': tokens.Keyword,
    'DATETIME_TRUNC': tokens.Keyword,
    'FORMAT_DATETIME': tokens.Keyword,
    'PARSE_DATETIME': tokens.Keyword,
    'CURRENT_TIME': tokens.Keyword,
    'TIME': tokens.Keyword,
    'TIME_ADD': tokens.Keyword,
    'TIME_SUB': tokens.Keyword,
    'TIME_DIFF': tokens.Keyword,
    'TIME_TRUNC': tokens.Keyword,
    'FORMAT_TIME': tokens.Keyword,
    'PARSE_TIME': tokens.Keyword,
    'CURRENT_TIMESTAMP': tokens.Keyword,
    'EXTRACT': tokens.Keyword,
    'STRING': tokens.Keyword,
    'TIMESTAMP': tokens.Keyword,
    'TIMESTAMP_ADD': tokens.Keyword,
    'TIMESTAMP_SUB': tokens.Keyword,
    'TIMESTAMP_DIFF': tokens.Keyword,
    'TIMESTAMP_TRUNC': tokens.Keyword,
    'FORMAT_TIMESTAMP': tokens.Keyword,
    'PARSE_TIMESTAMP': tokens.Keyword,
    'TIMESTAMP_SECONDS': tokens.Keyword,
    'TIMESTAMP_MILLIS': tokens.Keyword,
    'TIMESTAMP_MICROS': tokens.Keyword,
    'UNIX_SECONDS': tokens.Keyword,
    'UNIX_MILLIS': tokens.Keyword,
    'UNIX_MICROS': tokens.Keyword,
    'ST_GEOGPOINT': tokens.Keyword,
    'ST_MAKELINE': tokens.Keyword,
    'ST_MAKEPOLYGON': tokens.Keyword,
    'ST_MAKEPOLYGONORIENTED': tokens.Keyword,
    'ST_GEOGFROMGEOJSON': tokens.Keyword,
    'ST_GEOGFROMTEXT': tokens.Keyword,
    'ST_GEOGFROMWKB': tokens.Keyword,
    'ST_ASGEOJSON': tokens.Keyword,
    'ST_ASTEXT': tokens.Keyword,
    'ST_ASBINARY': tokens.Keyword,
    'ST_BOUNDARY': tokens.Keyword,
    'ST_CENTROID': tokens.Keyword,
    'ST_CLOSESTPOINT': tokens.Keyword,
    'ST_DIFFERENCE': tokens.Keyword,
    'ST_INTERSECTION': tokens.Keyword,
    'ST_SNAPTOGRID': tokens.Keyword,
    'ST_UNION': tokens.Keyword,
    'ST_X': tokens.Keyword,
    'ST_Y': tokens.Keyword,
    'ST_CONTAINS': tokens.Keyword,
    'ST_COVEREDBY': tokens.Keyword,
    'ST_COVERS': tokens.Keyword,
    'ST_DISJOINT': tokens.Keyword,
    'ST_DWITHIN': tokens.Keyword,
    'ST_EQUALS': tokens.Keyword,
    'ST_INTERSECTS': tokens.Keyword,
    'ST_INTERSECTSBOX': tokens.Keyword,
    'ST_TOUCHES': tokens.Keyword,
    'ST_WITHIN': tokens.Keyword,
    'ST_ISEMPTY': tokens.Keyword,
    'ST_ISCOLLECTION': tokens.Keyword,
    'ST_DIMENSION': tokens.Keyword,
    'ST_NUMPOINTS': tokens.Keyword,
    'ST_AREA': tokens.Keyword,
    'ST_DISTANCE': tokens.Keyword,
    'ST_LENGTH': tokens.Keyword,
    'ST_PERIMETER': tokens.Keyword,
    'SESSION_USER': tokens.Keyword,
    'GENERATE_UUID': tokens.Keyword,
    'NET.IP_FROM_STRING': tokens.Keyword,
    'NET.SAFE_IP_FROM_STRING': tokens.Keyword,
    'NET.IP_TO_STRING': tokens.Keyword,
    'NET.IP_NET_MASK': tokens.Keyword,
    'NET.IP_TRUNC': tokens.Keyword,
    'NET.IPV4_FROM_INT64': tokens.Keyword,
    'NET.IPV4_TO_INT64': tokens.Keyword,
    'NET.HOST': tokens.Keyword,
    'NET.PUBLIC_SUFFIX': tokens.Keyword,
    'NET.REG_DOMAIN': tokens.Keyword,
    'ERROR': tokens.Keyword,
}

KEYWORDS_ORACLE = {
    'ARCHIVE': tokens.Keyword,
    'ARCHIVELOG': tokens.Keyword,

    'BACKUP': tokens.Keyword,
    'BECOME': tokens.Keyword,
    'BLOCK': tokens.Keyword,
    'BODY': tokens.Keyword,

    'CANCEL': tokens.Keyword,
    'CHANGE': tokens.Keyword,
    'COMPILE': tokens.Keyword,
    'CONTENTS': tokens.Keyword,
    'CONTROLFILE': tokens.Keyword,

    'DATAFILE': tokens.Keyword,
    'DBA': tokens.Keyword,
    'DISMOUNT': tokens.Keyword,
    'DOUBLE': tokens.Keyword,
    'DUMP': tokens.Keyword,

    'EVENTS': tokens.Keyword,
    'EXCEPTIONS': tokens.Keyword,
    'EXPLAIN': tokens.Keyword,
    'EXTENT': tokens.Keyword,
    'EXTERNALLY': tokens.Keyword,

    'FLUSH': tokens.Keyword,
    'FREELIST': tokens.Keyword,
    'FREELISTS': tokens.Keyword,

    # groups seems too common as table name
    # 'GROUPS': tokens.Keyword,

    'INDICATOR': tokens.Keyword,
    'INITRANS': tokens.Keyword,
    'INSTANCE': tokens.Keyword,

    'LAYER': tokens.Keyword,
    'LINK': tokens.Keyword,
    'LISTS': tokens.Keyword,
    'LOGFILE': tokens.Keyword,

    'MANAGE': tokens.Keyword,
    'MANUAL': tokens.Keyword,
    'MAXDATAFILES': tokens.Keyword,
    'MAXINSTANCES': tokens.Keyword,
    'MAXLOGFILES': tokens.Keyword,
    'MAXLOGHISTORY': tokens.Keyword,
    'MAXLOGMEMBERS': tokens.Keyword,
    'MAXTRANS': tokens.Keyword,
    'MINEXTENTS': tokens.Keyword,
    'MODULE': tokens.Keyword,
    'MOUNT': tokens.Keyword,

    'NOARCHIVELOG': tokens.Keyword,
    'NOCACHE': tokens.Keyword,
    'NOCYCLE': tokens.Keyword,
    'NOMAXVALUE': tokens.Keyword,
    'NOMINVALUE': tokens.Keyword,
    'NOORDER': tokens.Keyword,
    'NORESETLOGS': tokens.Keyword,
    'NORMAL': tokens.Keyword,
    'NOSORT': tokens.Keyword,

    'OPTIMAL': tokens.Keyword,
    'OWN': tokens.Keyword,

    'PACKAGE': tokens.Keyword,
    'PARALLEL': tokens.Keyword,
    'PCTINCREASE': tokens.Keyword,
    'PCTUSED': tokens.Keyword,
    'PLAN': tokens.Keyword,
    'PRIVATE': tokens.Keyword,
    'PROFILE': tokens.Keyword,

    'QUOTA': tokens.Keyword,

    'RECOVER': tokens.Keyword,
    'RESETLOGS': tokens.Keyword,
    'RESTRICTED': tokens.Keyword,
    'REUSE': tokens.Keyword,
    'ROLES': tokens.Keyword,

    'SAVEPOINT': tokens.Keyword,
    'SCN': tokens.Keyword,
    'SECTION': tokens.Keyword,
    'SEGMENT': tokens.Keyword,
    'SHARED': tokens.Keyword,
    'SNAPSHOT': tokens.Keyword,
    'SORT': tokens.Keyword,
    'STATEMENT_ID': tokens.Keyword,
    'STOP': tokens.Keyword,
    'SWITCH': tokens.Keyword,

    'TABLES': tokens.Keyword,
    'TABLESPACE': tokens.Keyword,
    'THREAD': tokens.Keyword,
    'TIME': tokens.Keyword,
    'TRACING': tokens.Keyword,
    'TRANSACTION': tokens.Keyword,
    'TRIGGERS': tokens.Keyword,

    'UNLIMITED': tokens.Keyword,
    'UNLOCK': tokens.Keyword,
}

# PostgreSQL Syntax
KEYWORDS_PLPGSQL = {
    'PARTITION': tokens.Keyword,
    'OVER': tokens.Keyword,
    'PERFORM': tokens.Keyword,
    'NOTICE': tokens.Keyword,
    'PLPGSQL': tokens.Keyword,
    'INHERIT': tokens.Keyword,
    'INDEXES': tokens.Keyword,

    'BYTEA': tokens.Keyword,
    'BIGSERIAL': tokens.Keyword,
    'BIT VARYING': tokens.Keyword,
    'BOX': tokens.Keyword,
    'CHARACTER': tokens.Keyword,
    'CHARACTER VARYING': tokens.Keyword,
    'CIDR': tokens.Keyword,
    'CIRCLE': tokens.Keyword,
    'DOUBLE PRECISION': tokens.Keyword,
    'INET': tokens.Keyword,
    'JSON': tokens.Keyword,
    'JSONB': tokens.Keyword,
    'LINE': tokens.Keyword,
    'LSEG': tokens.Keyword,
    'MACADDR': tokens.Keyword,
    'MONEY': tokens.Keyword,
    'PATH': tokens.Keyword,
    'PG_LSN': tokens.Keyword,
    'POINT': tokens.Keyword,
    'POLYGON': tokens.Keyword,
    'SMALLSERIAL': tokens.Keyword,
    'TSQUERY': tokens.Keyword,
    'TSVECTOR': tokens.Keyword,
    'TXID_SNAPSHOT': tokens.Keyword,
    'UUID': tokens.Keyword,
    'XML': tokens.Keyword,

    'FOR': tokens.Keyword,
    'IN': tokens.Keyword,
    'LOOP': tokens.Keyword,
}