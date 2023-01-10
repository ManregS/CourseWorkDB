import psycopg2
import pandas as pd

class BankApp:
    def __init__(self, user, password):
        self.conn = psycopg2.connect(dbname="bank", user=user, password=password, host="localhost", port="5432")
        self.cur = self.conn.cursor()
    
    
    def getClients(self, block=False):
        if block == False:
            block = "where block = false"
        else:
            block = ""

        query = f"""
        select id_client, name
        from clients
        {block}
        """
        self.cur.execute(query)
        return dict([(client[0], client[1]) for client in self.cur.fetchall()])


    def getClientInfo(self, id_client):
        query = f"""
        select *
        from clients
        where id_client = {id_client}
        """
        self.cur.execute(query)
        
        data = self.cur.fetchone()

        info = f"""ID: {data[0]}
ФИО: {data[1]}
Дата рождения: {data[2]}
Серия: {data[3]}
Номер: {data[4]}
Баланс: {data[5]}"""
        return info


    def getClientTransfers(self, id_client):
        query = f"""
        select id, client_recip, amount, time_start
        from clients_transfers
        where client_init = {id_client}
        """
        self.cur.execute(query)
    
        return pd.DataFrame(self.cur.fetchall(), columns=["ID операции", "ID получателя", "Сумма", "Время выполнения"]).sort_values("Время выполнения")

    
    def getClientCredits(self, id_client):
        query = f"""
        select id, amount, time_start, maturity_date, status_return
        from clients_credits
        where client_init = {id_client}
        """
        self.cur.execute(query)
        return pd.DataFrame(self.cur.fetchall(), columns=["ID операции", "Сумма", "Время выдачи", "Дата погашения", "Статус возврата"]).sort_values("Время выдачи")
    

    def getClientMortgages(self, id_client):
        query = f"""
        select id, amount, time_start, maturity_date, address_prop, status_return
        from clients_mortgages
        where client_init = {id_client}
        """
        self.cur.execute(query)
        return pd.DataFrame(self.cur.fetchall(), columns=["ID операции", "Сумма", "Время выдачи", "Дата погашения", "Адрес собственности", "Статус возврата"]).sort_values("Время выдачи")


    def addClient(self, name, birth_date, series, number, cash, password):
        try:
            queryInsert = f"""
            insert into Clients (name, birth_date, series, number, cash, password)
            values ('{name}', '{birth_date}', {series}, {number}, '{cash}', md5('{password}'))
            """
            self.cur.execute(queryInsert)

            queryCreateClient = f"""
            create user "{name}" password '{password}'
            """
            self.cur.execute(queryCreateClient)

            queryGrant = f"""
            grant select on all tables in schema public to "{name}"
            """
            self.cur.execute(queryGrant)
            
            self.conn.commit()
            return ("Клиент успешно добавлен", "-")
        except:
            self.conn.rollback()
            return ("Ошибка добавления клиента", "warning")


    def moneyTransfer(self, client_init, client_recip, amount):
        try:
            queryOperation = f"""
            insert into operations (type, client_init)
            values ('money transfer', {client_init})
            returning id;
            """
            self.cur.execute(queryOperation)

            queryMoneyTransfer = f"""
            insert into money_transfers (id, client_recip, amount)
            values ({self.cur.fetchone()[0]}, {client_recip}, '{amount}')
            """
            self.cur.execute(queryMoneyTransfer)

            queryWriteOff = f"""
            update clients
            set cash = cash - '{amount}'
            where id_client = {client_init}
            """
            self.cur.execute(queryWriteOff)

            queryWriteOn = f"""
            update clients
            set cash = cash + '{amount}'
            where id_client = {client_recip}
            """
            self.cur.execute(queryWriteOn)

            self.conn.commit()
            return ("Средства успешно переведены", "-")
        except:
            self.conn.rollback()
            return ("Ошибка перевода средств", "warning")


    def addCredit(self, client_init, amount, maturity_date):
        try:
            queryOperation = f"""
            insert into operations (type, client_init)
            values ('credit', {client_init})
            returning id;
            """
            self.cur.execute(queryOperation)

            queryCredit = f"""
            insert into credits (id, amount, maturity_date)
            values ({self.cur.fetchone()[0]}, '{amount}', '{maturity_date}')
            """
            self.cur.execute(queryCredit)

            queryWriteOn = f"""
            update clients
            set cash = cash + '{amount}'
            where id_client = {client_init}
            """
            self.cur.execute(queryWriteOn)

            self.conn.commit()
            return ("Кредит успешно оформлен", "-")
        except:
            self.conn.rollback()
            return ("Ошибка оформления кредита", "warning")

    
    def addMortgage(self, client_init, amount, maturity_date, addres_prop):
        try:
            queryOperation = f"""
            insert into operations (type, client_init)
            values ('mortgage', {client_init})
            returning id;
            """
            self.cur.execute(queryOperation)

            queryMortgage = f"""
            insert into mortgages (id, amount, maturity_date, address_prop)
            values ({self.cur.fetchone()[0]}, '{amount}', '{maturity_date}', '{addres_prop}')
            """
            self.cur.execute(queryMortgage)

            self.conn.commit()
            return ("Ипотека успешно оформлена", "-")
        except:
            self.conn.rollback()
            return ("Ошибка оформления ипотеки", "warning")