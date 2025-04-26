import psycopg2

class DatabaseManager:
    def __init__(self, host, dbname, user, password, port):
        self.connection = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_list (
                id SERIAL PRIMARY KEY,
                product_name VARCHAR(255),
                product_brand VARCHAR(255),
                product_price TEXT,
                product_link TEXT,
                product_cons TEXT,
                product_pros TEXT,
                product_imp_feat TEXT,
                product_qa_key_points TEXT,
                product_crit_deta TEXT,
                product_recom TEXT,
                product_praises TEXT,
                product_complaints TEXT,
                product_sum_com TEXT,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.connection.commit()

    def insert_product(self, d, l, p, c):
        self.cursor.execute("""
            INSERT INTO product_list (
                product_name, product_brand, product_price, product_link,
                product_cons, product_pros, product_imp_feat,
                product_qa_key_points, product_crit_deta,
                product_recom, product_praises, product_complaints, product_sum_com
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            d['name'],
            d['brand'],
            d['price'],
            l,
            p.cons,
            p.pros,
            p.important_features,
            p.key_points_from_QA,
            p.crit_details,
            p.recommendations,
            c.praises,
            c.complaints,
            c.summary_of_comments
        ))
        self.connection.commit()


    def get_all_views(self):
        self.cursor.execute("SELECT * FROM product_list;")
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
