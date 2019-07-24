from flaskext.mysql import MySQL

# função para configurar o acesso a banco
def config(app):
    # Configurando o acesso ao MySQL
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'pcgo2013'
    app.config['MYSQL_DATABASE_DB'] = 'contatos'

# Retorna conexao e cursor
def get_db(mysql):
    # Obtendo o cursor para acessar o BD
    conn = mysql.connect()
    cursor = conn.cursor()

    return conn, cursor

def set_car(conn, cursor, marca, modelo, foto, preco, km, vip):
    cursor.execute(f'insert into carros (marca, modelo, km, vip, foto, preco) values ("{marca}", "{modelo}", "{km}", "{vip}", "{foto}", "{preco}");')
    conn.commit()

def vip_verifie(cursor):
    cursor.execute(f'select count(*) from carros where vip = 1')
    vips = cursor.fetchone()
    if vips is None:
        vips = 0
    return vips


def show_vips(cursor):
    cursor.execute(f'select idcarro, marca, modelo, km, vip, foto, preco from carros where vip = 1 and idcomp is NULL')
    vips = cursor.fetchall()
    return vips


def validate_login(cursor, login, senha):
    cursor.execute(f'select tipo, nome from usuarios where login = "{login}" and senha = "{senha}";')
    usuario = cursor.fetchone()
    if usuario:
        tipo = usuario[0]
        nome = usuario[1]
        return tipo, nome
    else:
        return None


def reservar_carro(conn, cursor, nome, cpf, tel, idcarro):
    cursor.execute(f'select idcomp from comp where cpf = "{cpf}";')
    existe = cursor.fetchone()
    if existe is None:
        cursor.execute(f'insert into comp (nome, cpf, tel) values ("{nome}", "{cpf}", "{tel}");')
        conn.commit()
    cursor.execute(f'select idcomp from comp where cpf = "{cpf}";')
    idcomprador = cursor.fetchone()[0]
    cursor.execute(f'update carros set idcomprador = {idcomprador} where idcarro = {idcarro}')
    conn.commit()


def show_all_cars(cursor):
    cursor.execute(f'select * from carros')
    carros = cursor.fetchall()
    return carros