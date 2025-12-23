import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import sys


def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


if len(sys.argv) != 2:
    print("错误：请指定日期参数，格式为YYYY-MM-DD")
    print("示例：python export_assessment.py 2025-04-08")
    sys.exit(1)


# 修改为你的数据库配置（使用SQLAlchemy格式）
DB_CONFIG = {
    'dialect': 'mysql',
    'driver': 'pymysql',
    'username': 'cmbh',
    'password': 'cmbhW2vuwDEQJRFrL!sO',
    'host': '10.29.222.18',
    'port': 4000,
    'database': 'cnpc',
    'charset': 'utf8mb4',
}

# 生成SQLAlchemy连接URI
db_uri = (
    f"{DB_CONFIG['dialect']}+{DB_CONFIG['driver']}://"
    f"{DB_CONFIG['username']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/"  # 添加端口号
    f"{DB_CONFIG['database']}?charset={DB_CONFIG['charset']}"
)

# 参数化SQL（防止SQL注入）
sql = """
SELECT
    t.create_date AS 'date',
    t.call_id AS 'callid',
    t.`session` AS 'session',
    t.assessment AS '评价情况',
    t.channel AS '接入渠道'
FROM
    bus_assessment_info t
WHERE
    t.create_date BETWEEN %s AND %s
    AND t.business_type = %s
ORDER BY
    t.create_date;
"""


def export_xlsx(input_date, start_time, end_time, business_type, business_name):

    # 创建SQLAlchemy引擎
    engine = create_engine(db_uri)

    try:
        # 执行查询
        df = pd.read_sql(sql, engine, params=(start_time, end_time, business_type))

        # 调试：显示前3行数据
        print("\n[DEBUG] 查询结果样例：")
        print(df.head(3) if not df.empty else "无数据")

        if df.empty:
            print(f"警告：{start_time} 无符合条件的数据")
        else:
            print(f"成功读取 {len(df)} 条记录")

        # 导出Excel
        output_filename = f"{input_date}-{business_name}.xlsx"
        df.to_excel(output_filename, index=False, engine='openpyxl')
        print(f"文件已生成：{output_filename}")

    except Exception as e:
        print(f"操作失败：{str(e)}")
        sys.exit(1)

    finally:
        engine.dispose()  # 关闭连接池


if __name__ == '__main__':

    input_date = sys.argv[1]
    if not validate_date(input_date):
        print("错误：日期格式无效，请使用YYYY-MM-DD格式")
        sys.exit(1)

    # 时间范围
    start_time = f"{input_date} 00:00:01"
    end_time = f"{input_date} 23:59:59"

    # business_type：0:会话摘要 1:话术推荐 2:话术小结
    # business_type = 0
    # business_name = '会话摘要'

    export_xlsx(input_date, start_time, end_time, 0, '会话摘要')
    export_xlsx(input_date, start_time, end_time, 1, '话术推荐')
    export_xlsx(input_date, start_time, end_time, 2, '话术小结')
