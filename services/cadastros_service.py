from database.db import query_df, execute

def get_maquinas():
    return query_df("SELECT * FROM maquinas ORDER BY nome")

def get_produtos():
    return query_df("SELECT * FROM produtos ORDER BY descricao")

def get_motivos():
    return query_df("SELECT * FROM motivos_qualidade ORDER BY descricao")

def add_produto(codigo, descricao, familia, unidade):
    execute('INSERT INTO produtos (codigo, descricao, familia, unidade) VALUES (:codigo,:descricao,:familia,:unidade)',
            {"codigo":codigo,"descricao":descricao,"familia":familia,"unidade":unidade})

def update_produto(produto_id, codigo, descricao, familia, unidade, ativo=1):
    execute('UPDATE produtos SET codigo=:codigo, descricao=:descricao, familia=:familia, unidade=:unidade, ativo=:ativo WHERE id=:id',
            {"id": produto_id, "codigo":codigo,"descricao":descricao,"familia":familia,"unidade":unidade,"ativo":ativo})

def delete_produto(produto_id):
    execute('DELETE FROM produtos WHERE id = :id', {"id": produto_id})

def add_motivo(descricao, categoria):
    execute('INSERT INTO motivos_qualidade (descricao, categoria) VALUES (:descricao,:categoria)',
            {"descricao":descricao,"categoria":categoria})

def add_maquina(nome, processo):
    execute('INSERT INTO maquinas (nome, processo) VALUES (:nome,:processo)', {"nome": nome, "processo": processo})

def update_maquina(maquina_id, nome, processo, ativo=1):
    execute('UPDATE maquinas SET nome=:nome, processo=:processo, ativo=:ativo WHERE id=:id',
            {"id": maquina_id, "nome": nome, "processo": processo, "ativo": ativo})

def delete_maquina(maquina_id):
    execute('DELETE FROM maquinas WHERE id = :id', {"id": maquina_id})
