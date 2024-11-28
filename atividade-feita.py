import os
os.system("cls || clear")
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()
engine = create_engine("sqlite:///rh_system.db")
Session = sessionmaker(bind=engine)
session = Session()

class Funcionario(Base):
    __tablename__ = "funcionarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    setor = Column(String, nullable=False)
    funcao = Column(String, nullable=False)
    salario = Column(Float, nullable=False)
    telefone = Column(String, nullable=False)


Base.metadata.create_all(engine)

# Definindo funcoes 
def salvar_funcionario(funcionario):
    session.add(funcionario)
    session.commit()

def listar_todos_funcionarios():
    return session.query(Funcionario).all()

def pesquisar_um_funcionario(cpf):
    return session.query(Funcionario).filter_by(cpf=cpf).first()

def atualizar_funcionario(cpf, novos_dados):
    funcionario = pesquisar_um_funcionario(cpf)
    if funcionario:
        for chave, valor in novos_dados.items():
            setattr(funcionario, chave, valor)
        session.commit()

def excluir_funcionario(cpf):
    funcionario = pesquisar_um_funcionario(cpf)
    if funcionario:
        session.delete(funcionario)
        session.commit()

# Sistema Interativo
def menu():
    while True:
        print("\n=== RH System ===")
        print("1 - Adicionar funcionário")
        print("2 - Consultar um funcionário")
        print("3 - Atualizar os dados de um funcionário")
        print("4 - Excluir um funcionário")
        print("5 - Listar todos os funcionários")
        print("0 - Sair do sistema")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            idade = int(input("Idade: "))
            cpf = input("CPF: ")
            setor = input("Setor: ")
            funcao = input("Função: ")
            salario = float(input("Salário: "))
            telefone = input("Telefone: ")
            funcionario = Funcionario(nome=nome, idade=idade, cpf=cpf, setor=setor, funcao=funcao, salario=salario, telefone=telefone)
            salvar_funcionario(funcionario)
            print("Funcionário adicionado com sucesso!")

        elif opcao == "2":
            cpf = input("CPF do funcionário: ")
            funcionario = pesquisar_um_funcionario(cpf)
            if funcionario:
                print(f"Nome: {funcionario.nome}, Idade: {funcionario.idade}, CPF: {funcionario.cpf}, Setor: {funcionario.setor}, Função: {funcionario.funcao}, Salário: {funcionario.salario}, Telefone: {funcionario.telefone}")
            else:
                print("Funcionário não encontrado.")

        elif opcao == "3":
            cpf = input("CPF do funcionário: ")
            novos_dados = {}
            print("Deixe em branco para manter o dado atual.")
            novos_dados["nome"] = input("Novo nome: ") or None
            novos_dados["idade"] = input("Nova idade: ") or None
            novos_dados["setor"] = input("Novo setor: ") or None
            novos_dados["funcao"] = input("Nova função: ") or None
            novos_dados["salario"] = input("Novo salário: ") or None
            novos_dados["telefone"] = input("Novo telefone: ") or None
            novos_dados = {k: v for k, v in novos_dados.items() if v}
            atualizar_funcionario(cpf, novos_dados)
            print("Funcionário atualizado com sucesso!")

        elif opcao == "4":
            cpf = input("CPF do funcionário: ")
            excluir_funcionario(cpf)
            print("Funcionário excluído com sucesso!")

        elif opcao == "5":
            funcionarios = listar_todos_funcionarios()
            for f in funcionarios:
                print(f"ID: {f.id}, Nome: {f.nome}, CPF: {f.cpf}")

        elif opcao == "0":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
