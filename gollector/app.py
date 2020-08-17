import yaml
import psycopg2
from gollector.domain import FQDN_Features


def get_config():
    config = open("config.yml")
    return yaml.load(config)


class DomainFeatures:

    def __init__(self, config):
        self.config = config
        self.conn = self.connect_db()
        self.batch_size = 2
        self.inserts = list()
        self.create_table()

    def connect_db(self):
        conn = psycopg2.connect(
            host=self.config["host"],
            database=self.config["dbname"],
            port=self.config["port"],
            user=self.config["user"],
            password=self.config["password"])
        return conn

    def create_table(self):
        try:
            c = self.conn.cursor()
            c.execute("create table if not exists fqdn_features ("
                            "fqdn_id int primary key, "
                            "label_number int, "
                            "lenght int, "
                            "entropy numeric, "
                            "vowels_ratio numeric, "
                            "vowels_number int, "
                            "consonants_ratio numeric, "
                            "consonants_number int, "
                            "numeric_ratio numeric, "
                            "numeric_number int, "
                            "special_ratio numeric, "
                            "special_number numeric);")
            self.conn.commit()
            c.close()
        except Exception as e:
            print(e)

    def insert(self):
        cursor = self.conn.cursor()

        query = cursor.mogrify("INSERT INTO {} ({}) VALUES {}".format(
            "fqdn_features",
            ', '.join(self.inserts[0].keys()),
            ', '.join(['%s'] * len(self.inserts))
        ), [tuple(v.values()) for v in self.inserts])

        cursor.execute(query)

        self.conn.commit()
        cursor.close()
        self.inserts = list()

    def run_gollector(self):
        cursor = self.conn.cursor()

        cursor.execute("select count(*) as count from fqdns")
        domain_count = cursor.fetchall()
        for offset in range(0, domain_count[0][0], self.batch_size):

            cc = self.conn.cursor()
            cc.execute("select id, fqdn from fqdns limit %s offset %s", (self.batch_size, offset,))
            fqdns = cc.fetchall()

            for fqdn in fqdns:
                f = FQDN_Features(fqdn[0], fqdn[1])
                self.inserts.append(f.get_features())
            cc.close()
            self.insert()


def main():
    conf = get_config()
    df = DomainFeatures(conf)
    df.run_gollector()
    #todo make run function about buldozer


if __name__ == '__main__':
    main()

