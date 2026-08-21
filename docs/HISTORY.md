# Histórico de decisões arquiteturais

Este arquivo explica decisões passadas; não é uma fonte operacional superior à governança, configuração ou código atuais.

## Hermes Bridge

O Bridge foi criado quando se acreditava que a delegação nativa não permitia selecionar modelo/provider diferente do Gerente. Testes posteriores comprovaram override nativo e tornaram o Bridge desnecessário no fluxo principal.

Decisão atual: preferir capacidade nativa comprovada. Preservar o Bridge apenas como precedente para a regra “investigar upstream antes de workaround”.

## Roteamento por complexidade

A política antiga “simples = Flash; complexo = Pro” foi substituída. O Flash demonstrou qualidade em auditoria e análise avançada, mas isso não prova capacidade universal.

Decisão atual: usar o executor mais econômico comprovadamente capaz e escalar por evidência; complexidade orienta decomposição, enquanto risco orienta validação.

## Benchmark de delegação nativa

Os benchmarks originaram práticas incorporadas nas skills canônicas: tarefa autocontida, veredito primeiro, fato versus hipótese, evidência verificável, metadados reais da delegação, revisão independente dos pontos críticos e tratamento de truncamento.

O draft separado foi encerrado após essa incorporação. Regras específicas de benchmark não viraram obrigações universais.

## Consolidação documental de 2026-08-21

Após leitura integral do projeto, o conteúdo operacional foi reduzido de 36 Markdown (158.352 bytes) para 17 Markdown canônicos (aproximadamente 28 KB).

Foram fundidos na governança, arquitetura, skills, templates e neste histórico:

- o consolidado e as propostas Gerente–Executor;
- o kit genérico V2 experimental;
- a regra upstream/reset de hipóteses;
- os manuais antigos de arquitetura, fluxo e roadmap;
- o draft de benchmark de delegação nativa.

Foram removidos como redundantes ou obsoletos: cópias exatas na raiz, documentos do Bridge, guia do antigo `streamrank-manager`, arquivos vazios e specs duplicadas. O handoff do OsModerna e a checklist antiga do Bridge foram retirados por serem estado específico/histórico de outro projeto, não governança genérica.

Os arquivos anteriores foram preservados em backup recuperável fora do repositório antes da limpeza.
