# 💰 Automação Financeira — Controle e Análise

> Sistema de controle financeiro pessoal com lançamentos categorizados, análise de cenários, gráfico de despesas por categoria e relatórios exportáveis — desenvolvido em Python puro.

---

## 🧩 Contexto de Negócio

A falta de visibilidade sobre receitas e despesas é um dos principais obstáculos para o planejamento financeiro eficiente — tanto para pessoas físicas quanto para pequenas operações. Planilhas manuais são propensas a erros e não oferecem análise automatizada.

Este projeto nasceu de uma necessidade real: automatizar o registro e a categorização de lançamentos financeiros, eliminar o trabalho manual de conciliação e gerar análises que apoiem decisões de corte de custos ou aumento de receita.

**Problema resolvido:** substituir o controle manual em planilhas por um sistema automatizado que categoriza lançamentos, calcula saldo em tempo real e simula cenários financeiros futuros.

---

## 🎯 Funcionalidades

- Lançamentos de receitas e despesas com categorização automática
- Resumo financeiro em tempo real com alerta de saldo negativo
- Análise por categoria com gráfico de barras no terminal
- Simulação de cenários: impacto de redução de despesas (5% a 30%) e aumento de receita
- Exportação de relatório completo em `.txt`
- Persistência em JSON entre sessões

---

## 🗂️ Dicionário de Dados

Cada lançamento é armazenado em `financeiro.json`:

| Campo        | Tipo     | Descrição                                           |
|-------------|----------|-----------------------------------------------------|
| `id`         | int      | Identificador único do lançamento                   |
| `tipo`       | string   | Receita ou Despesa                                  |
| `categoria`  | string   | Categoria do lançamento (ver tabelas abaixo)        |
| `descricao`  | string   | Descrição livre do lançamento                       |
| `valor`      | float    | Valor positivo em reais                             |
| `data`       | date     | Data do lançamento (DD/MM/AAAA)                     |
| `criado_em`  | datetime | Timestamp de registro no sistema                   |

**Categorias disponíveis:**

| Receitas       | Despesas      |
|----------------|---------------|
| Salário        | Moradia       |
| Freelance      | Alimentação   |
| Investimentos  | Transporte    |
| Vendas         | Saúde         |
| Outros         | Educação      |
|                | Lazer         |
|                | Serviços      |
|                | Impostos      |
|                | Outros        |

---

## 💡 Análise de Cenários — Exemplo

```
  Cenário                   Redução        Novo Saldo
  ──────────────────────────────────────────────────
  Reduzir despesas 5%     R$ 160,00    R$ 1.960,00
  Reduzir despesas 10%    R$ 320,00    R$ 2.120,00
  Reduzir despesas 15%    R$ 480,00    R$ 2.280,00
  Reduzir despesas 20%    R$ 640,00    R$ 2.440,00
  Reduzir despesas 30%    R$ 960,00    R$ 2.760,00
  ──────────────────────────────────────────────────
  Aumentar receita 5%     R$ 250,00    R$ 2.050,00
  Aumentar receita 10%    R$ 500,00    R$ 2.300,00
  Aumentar receita 20%  R$ 1.000,00    R$ 2.800,00
```

---

## 🚀 Como executar

```bash
# Clone o repositório
git clone https://github.com/rosariodutra/automacao-financeira.git
cd automacao-financeira

# Sem dependências externas — Python 3.6+ puro
python automacao_financeira.py
```

> Os dados são salvos automaticamente em `financeiro.json` na mesma pasta.

---

## 🛠️ Tecnologias

![Python](https://img.shields.io/badge/Python-7c3aed?style=flat-square&logo=python&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-6d28d9?style=flat-square&logo=json&logoColor=white)

---

## 👩‍💻 Autora

Feito com 💜 por [Rosário Dutra](https://github.com/rosariodutra) · Analista de Dados & BI
