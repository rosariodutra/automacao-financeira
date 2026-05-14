# =============================================================
#  💰 AUTOMAÇÃO FINANCEIRA
#  Autor: Rosário Dutra
#  GitHub: github.com/rosariodutra
#  Descrição: Sistema de controle financeiro com lançamentos,
#             categorização, análise de cenários e relatórios.
# =============================================================

import os
import json
from datetime import datetime

# ── Arquivo de dados ──────────────────────────────────────────
ARQUIVO = "financeiro.json"

# ── Cores ─────────────────────────────────────────────────────
ROXO     = "\033[35m"
VERDE    = "\033[32m"
AMARELO  = "\033[33m"
VERMELHO = "\033[31m"
RESET    = "\033[0m"
NEGRITO  = "\033[1m"

# ── Categorias ────────────────────────────────────────────────
CATEGORIAS_RECEITA = ["Salário", "Freelance", "Investimentos", "Vendas", "Outros"]
CATEGORIAS_DESPESA = ["Moradia", "Alimentação", "Transporte", "Saúde", "Educação",
                      "Lazer", "Serviços", "Impostos", "Outros"]

# ── Persistência ──────────────────────────────────────────────

def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar(lancamentos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(lancamentos, f, ensure_ascii=False, indent=2)

# ── Utilitários ───────────────────────────────────────────────

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def cabecalho():
    print(f"{ROXO}")
    print("╔══════════════════════════════════════════╗")
    print("║       💰  AUTOMAÇÃO FINANCEIRA  💰         ║")
    print("║        github.com/rosariodutra            ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{RESET}")

def agora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def formatar_valor(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def proximo_id(lancamentos):
    return max((l["id"] for l in lancamentos), default=0) + 1

def escolher_categoria(tipo):
    cats = CATEGORIAS_RECEITA if tipo == "Receita" else CATEGORIAS_DESPESA
    print(f"\n  Categorias de {tipo}:\n")
    for i, c in enumerate(cats, 1):
        print(f"    {i}. {c}")
    while True:
        op = input("\n  Opção: ").strip()
        if op.isdigit() and 1 <= int(op) <= len(cats):
            return cats[int(op)-1]
        print("  ⚠️  Opção inválida!")

def entrada_valor(msg):
    while True:
        try:
            v = float(input(f"  {msg}: ").strip().replace(",", "."))
            if v <= 0:
                print("  ⚠️  Valor deve ser positivo!")
                continue
            return v
        except ValueError:
            print("  ⚠️  Digite um valor válido!")

# ── Resumo financeiro ─────────────────────────────────────────

def resumo(lancamentos):
    receitas  = sum(l["valor"] for l in lancamentos if l["tipo"] == "Receita")
    despesas  = sum(l["valor"] for l in lancamentos if l["tipo"] == "Despesa")
    saldo     = receitas - despesas
    cor_saldo = VERDE if saldo >= 0 else VERMELHO

    print(f"  {'─'*44}")
    print(f"  {'RESUMO FINANCEIRO':^44}")
    print(f"  {'─'*44}")
    print(f"  {'Total de Receitas':<28} {VERDE}{formatar_valor(receitas):>14}{RESET}")
    print(f"  {'Total de Despesas':<28} {VERMELHO}{formatar_valor(despesas):>14}{RESET}")
    print(f"  {'─'*44}")
    print(f"  {NEGRITO}{'Saldo':<28} {cor_saldo}{formatar_valor(saldo):>14}{RESET}")
    print(f"  {'─'*44}\n")

    if saldo < 0:
        print(f"  {VERMELHO}⚠️  Saldo negativo! Revise suas despesas.{RESET}\n")
    elif saldo == 0:
        print(f"  {AMARELO}⚡ Saldo zerado. Atenção ao orçamento!{RESET}\n")
    else:
        pct = (saldo / receitas * 100) if receitas > 0 else 0
        print(f"  {VERDE}✅ Você está guardando {pct:.1f}% da receita.{RESET}\n")

# ── Novo lançamento ───────────────────────────────────────────

def novo_lancamento(lancamentos):
    limpar(); cabecalho()
    print("  ── Novo Lançamento ──\n")
    print("  1. Receita\n  2. Despesa\n")

    op = input("  Tipo: ").strip()
    if op not in ("1", "2"):
        print("  ⚠️  Inválido!"); input("  [Enter]"); return

    tipo = "Receita" if op == "1" else "Despesa"
    categoria = escolher_categoria(tipo)

    limpar(); cabecalho()
    descricao = input("  Descrição: ").strip()
    valor = entrada_valor("Valor (R$)")

    # Data
    data_str = input("  Data (DD/MM/AAAA) ou Enter para hoje: ").strip()
    if not data_str:
        data = datetime.now().strftime("%d/%m/%Y")
    else:
        try:
            datetime.strptime(data_str, "%d/%m/%Y")
            data = data_str
        except:
            print("  ⚠️  Data inválida, usando hoje.")
            data = datetime.now().strftime("%d/%m/%Y")

    lancamento = {
        "id":        proximo_id(lancamentos),
        "tipo":      tipo,
        "categoria": categoria,
        "descricao": descricao,
        "valor":     valor,
        "data":      data,
        "criado_em": agora(),
    }
    lancamentos.append(lancamento)
    salvar(lancamentos)

    cor = VERDE if tipo == "Receita" else VERMELHO
    print(f"\n  {cor}✅ {tipo} de {formatar_valor(valor)} registrada!{RESET}\n")
    input("  [Enter para continuar]")

# ── Listar lançamentos ────────────────────────────────────────

def listar(lancamentos, filtro_tipo=None, filtro_cat=None):
    limpar(); cabecalho()

    lista = lancamentos
    if filtro_tipo:
        lista = [l for l in lista if l["tipo"] == filtro_tipo]
    if filtro_cat:
        lista = [l for l in lista if l["categoria"] == filtro_cat]

    if not lista:
        print("  Nenhum lançamento encontrado.\n")
        input("  [Enter para voltar]"); return

    print(f"  {'ID':<5} {'Data':<12} {'Tipo':<10} {'Categoria':<15} {'Descrição':<20} {'Valor':>12}")
    print(f"  {'─'*76}")
    for l in lista:
        cor = VERDE if l["tipo"] == "Receita" else VERMELHO
        print(f"  {l['id']:<5} {l['data']:<12} {l['tipo']:<10} {l['categoria']:<15} "
              f"{l['descricao'][:19]:<20} {cor}{formatar_valor(l['valor']):>12}{RESET}")
    print()
    input("  [Enter para voltar]")

# ── Análise por categoria ─────────────────────────────────────

def analise_categorias(lancamentos):
    limpar(); cabecalho()
    print("  ── Análise por Categoria ──\n")

    despesas = [l for l in lancamentos if l["tipo"] == "Despesa"]
    if not despesas:
        print("  Nenhuma despesa registrada.\n")
        input("  [Enter]"); return

    total = sum(l["valor"] for l in despesas)
    por_cat = {}
    for l in despesas:
        por_cat[l["categoria"]] = por_cat.get(l["categoria"], 0) + l["valor"]

    por_cat_sorted = sorted(por_cat.items(), key=lambda x: x[1], reverse=True)

    print(f"  {'Categoria':<20} {'Valor':>12}  {'%':>6}  Barra")
    print(f"  {'─'*60}")
    for cat, val in por_cat_sorted:
        pct = val / total * 100
        barra = "█" * int(pct / 5)
        print(f"  {cat:<20} {formatar_valor(val):>12}  {pct:>5.1f}%  {ROXO}{barra}{RESET}")

    print(f"\n  {'─'*60}")
    print(f"  {'TOTAL':<20} {VERMELHO}{formatar_valor(total):>12}{RESET}\n")

    # Maior despesa
    maior = max(por_cat_sorted, key=lambda x: x[1])
    print(f"  {AMARELO}💡 Maior gasto: {maior[0]} ({formatar_valor(maior[1])}){RESET}\n")
    input("  [Enter para voltar]")

# ── Análise de cenários ───────────────────────────────────────

def analise_cenarios(lancamentos):
    limpar(); cabecalho()
    print("  ── Análise de Cenários ──\n")

    receitas = sum(l["valor"] for l in lancamentos if l["tipo"] == "Receita")
    despesas = sum(l["valor"] for l in lancamentos if l["tipo"] == "Despesa")
    saldo    = receitas - despesas

    if receitas == 0:
        print("  Sem receitas registradas para análise.\n")
        input("  [Enter]"); return

    print(f"  Base atual: Receitas {formatar_valor(receitas)} | "
          f"Despesas {formatar_valor(despesas)} | Saldo {formatar_valor(saldo)}\n")
    print(f"  {'─'*50}")
    print(f"  {'Cenário':<25} {'Redução':<10} {'Novo Saldo':>14}")
    print(f"  {'─'*50}")

    for pct in [5, 10, 15, 20, 30]:
        economia = despesas * (pct / 100)
        novo_saldo = saldo + economia
        cor = VERDE if novo_saldo >= 0 else VERMELHO
        print(f"  {f'Reduzir despesas {pct}%':<25} {formatar_valor(economia):<10}  "
              f"{cor}{formatar_valor(novo_saldo):>14}{RESET}")

    print(f"\n  {'─'*50}")
    print(f"  {'Cenário':<25} {'Aumento':<10} {'Novo Saldo':>14}")
    print(f"  {'─'*50}")

    for pct in [5, 10, 20]:
        aumento = receitas * (pct / 100)
        novo_saldo = saldo + aumento
        cor = VERDE if novo_saldo >= 0 else VERMELHO
        print(f"  {f'Aumentar receita {pct}%':<25} {formatar_valor(aumento):<10}  "
              f"{cor}{formatar_valor(novo_saldo):>14}{RESET}")

    print()
    input("  [Enter para voltar]")

# ── Exportar relatório ────────────────────────────────────────

def exportar(lancamentos):
    nome = f"relatorio_financeiro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    receitas = sum(l["valor"] for l in lancamentos if l["tipo"] == "Receita")
    despesas = sum(l["valor"] for l in lancamentos if l["tipo"] == "Despesa")

    with open(nome, "w", encoding="utf-8") as f:
        f.write("RELATÓRIO FINANCEIRO — Automação Financeira by Rosário Dutra\n")
        f.write(f"Gerado em: {agora()}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"RESUMO\n")
        f.write(f"Receitas : R$ {receitas:,.2f}\n")
        f.write(f"Despesas : R$ {despesas:,.2f}\n")
        f.write(f"Saldo    : R$ {receitas-despesas:,.2f}\n\n")
        f.write("LANÇAMENTOS\n" + "-"*60 + "\n")
        for l in lancamentos:
            f.write(f"{l['data']} | {l['tipo']:<10} | {l['categoria']:<15} | "
                    f"{l['descricao']:<25} | R$ {l['valor']:,.2f}\n")

    print(f"\n  {VERDE}✅ Relatório exportado: {nome}{RESET}\n")
    input("  [Enter para continuar]")

# ── Menu principal ────────────────────────────────────────────

def main():
    lancamentos = carregar()

    while True:
        limpar(); cabecalho()
        resumo(lancamentos)

        print("  1. Novo lançamento")
        print("  2. Listar todos")
        print("  3. Listar receitas")
        print("  4. Listar despesas")
        print("  5. Análise por categoria")
        print("  6. Análise de cenários")
        print("  7. Exportar relatório (.txt)")
        print("  0. Sair\n")

        op = input("  Opção: ").strip()

        if op == "1":   novo_lancamento(lancamentos)
        elif op == "2": listar(lancamentos)
        elif op == "3": listar(lancamentos, filtro_tipo="Receita")
        elif op == "4": listar(lancamentos, filtro_tipo="Despesa")
        elif op == "5": analise_categorias(lancamentos)
        elif op == "6": analise_cenarios(lancamentos)
        elif op == "7": exportar(lancamentos)
        elif op == "0":
            limpar(); cabecalho()
            print("  Até logo! 💜\n"); break
        else:
            print("  ⚠️  Opção inválida!"); input("  [Enter]")

if __name__ == "__main__":
    main()
