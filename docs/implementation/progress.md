# Progresso PetLand 3.0

## Estado desta entrega

**Atual:** fechamento da release de portfólio/demo 3.0.0, schema `0007_product_operations`, por `release/petland-3.0` → `main`. PR #13 integrado em `968a1451beaa2587764a97d1d257adf597223dff`; legado `3cc3f898cde896b80fed587bf8c06f4aa46742f6` preservado em branch/tag. [Pedido](Portfolio-closure-request.txt), [registro](../evidence/Portfolio-closure.md) e [notas](../release/3.0.0.md). Produção comercial, aceite humano/leitor de tela e D10 continuam pendentes. Os registros abaixo preservam seus estados históricos.

| Card   | Escopo / requisitos                                             | Estado e evidência                                                                                                           |
| ------ | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| PL3-01 | Histórico, fontes oficiais, ADRs e gates                        | Concluído, commit `80afeaa`; docs/product, ux, adr, migration                                                                |
| PL3-02 | API/web/DB/Compose/contratos/CI, RF13, RNF05/07/09              | Concluído; verificações locais, CI e clone limpo aprovados                                                                   |
| PL3-03 | Tokens, navegação e campos acessíveis, RF13/RNF04               | Concluído; galeria funcional, 4 testes React e 6 E2E aprovados                                                               |
| PL3-04 | Sessão/login/logout e CSRF; RF01/RNF01                          | Concluído; revogação/CSRF/propriedade, React/API/PostgreSQL e E2E aprovados                                                  |
| PL3-05 | Cadastro/verificação/reset; RF01/RNF01                          | Concluído; SMTP/Mailpit real, uso único e consumo concorrente verificados                                                    |
| PL3-06 | Convites/papéis/bootstrap; RF01/RNF01                           | Concluído; D07, reautenticação, versão, auditoria e último admin sob concorrência                                            |
| PL3-07 | Perfil mínimo, cadastro assistido e associação verificada; RF02 | Implementado; vínculo de uso único, e-mail confirmado e isolamento                                                           |
| PL3-08 | Pets, referências, edição/arquivo; RF03/RNF01/04                | Implementado; propriedade A/B, FK raça/espécie, versão, preservação                                                          |
| PL3-09 | Serviços/ofertas por porte e catálogo público; RF04/RF12        | Implementado; Decimal BRL, duração, compatibilidade, ativo/inativo, catálogo/landing/dashboard                               |
| PL3-10 | Calendário, recursos, pausas/exceções; RF05                     | Implementado; interseção loja/pessoa e impacto revalidado ao salvar                                                          |
| PL3-11 | Disponibilidade e reserva; RF06/RNF06                           | Implementado; lock, duas exclusões GiST, snapshots, idempotência e testes concorrentes                                       |
| PL3-12 | Jornada de agendamento; RF06/RNF04/06                           | Implementado; resumo do servidor, confirmação, 409 sem perder escolhas, repetição após resposta perdida                      |
| PL3-13 | Cancelar/reagendar; RF07                                        | Implementado; versão, prazo contratado, assistência, rollback, eventos e avisos SMTP persistentes                            |
| PL3-14 | Agenda e execução, RF08/RNF01/04/06                             | Implementado; dia/semana/filtros, transições, instantes reais, falta, extensão e proteção de ocupação                        |
| PL3-15 | Notas e histórico, RF09/RNF01                                   | Implementado; autoria, append-only, visibilidade explícita, resumo próprio sem notas internas                                |
| PL3-16 | Gestão/configuração, RF10/RF07                                  | Implementado; impacto protege execução aberta, calendário até meia-noite, identificação pública e gestão existente integrada |
| PL3-17 | Indicadores/auditoria, RF11                                     | Implementado; fórmulas documentadas, limites de período, capacidade atual e consulta ADMIN paginada                          |
| PL3-18 | P06, RNF01–04/06/07                                             | Integrado pelo usuário; CI/medições aprovadas, aceite humano com leitor de tela ainda pendente                               |
| PL3-19 | Mapeamento/migração condicionais                                | Dispensados por D08/D12; nenhum MySQL acessado ou histórico importado                                                        |
| PL3-20 | Dados/ensaio operacional P07                                    | PR #7 integrado; checks/browser/operations aprovados; demo e restore comprovados, publicação externa adiada D10              |
| PL3-21 | P08, release/case                                               | Candidata, case, antes/depois, vídeo, diagramas e pacote local preparados; aceite final/publicação estável pendentes         |

Arquivos principais: `apps/api/src/petland/bootstrap/app.py`, módulo técnico `system`, `apps/api/migrations`, `apps/web/src/features`, `apps/web/src/shared`, `packages/api-contract`, `infra`, `.github/workflows/ci.yml`, `scripts/dev.py`, README e AGENTS.md.

## Aceite da primeira entrega

1. Histórico preservado por tag e mesmo repositório.
2. Monorepo na estrutura aprovada, sem legado/venv no código ativo.
3. FastAPI inicia e responde health/readiness.
4. React inicia; rotas e reload direto funcionam.
5. Comunicação web/API/DB verificada por E2E.
6. PostgreSQL local iniciado.
7. Migrations executadas, repetidas e revertidas em teste.
8. Design system funcional, sem persistência simulada.
9. Fronteiras verificadas e guard testado contra violações.
10. Testes: 18 Python + 4 React + 6 E2E aprovados.
11. Build frontend aprovado.
12. README validado em clone limpo: `init` e `up`, banco novo, migrations e serviços saudáveis.
13. Contratos reais gerados; identidade/reserva documentadas como futuras.
14. AGENTS.md criado.
15. Plano/PDF integrais incorporados com hashes registrados.
16. Nenhum segredo real adicionado; .env local ignorado; scan inicial passou.
17. Funcionalidades posteriores identificadas como planejadas.

## Decisões / impedimentos / continuidade

Decisões D01–D11 respondidas no pedido P03; pontos incompletos seguem as recomendações por autorização expressa. Registro vigente em docs/product/decisions.md. D08 dispensa migração de dados legados; D10 adia publicação/provedor.

Card atual: **PL3-21**, fase P08 autorizada em [P08-request.txt](P08-request.txt), sobre P07 integrada. Continuidade não comprova aceite sonoro/final humano. [ADR-015](../adr/0015-p08-release-case.md) mantém candidata explícita e [procedimento de revisão](../runbooks/release.md). D08/D12 dispensam migração; D10 mantém provedor, publicação e backup externo adiados. Não publicar/taguear/promover ou iniciar escopo adicional automaticamente.

Docker recuperado após reinício autorizado do Windows em 30/09/2026; em 01/10/2026 os serviços voltaram saudáveis, preservando volumes e dados. A falha anterior do backend OTel/socket residual não reapareceu. Saltos de relógio WSL de cerca de cinco segundos foram observados; a sincronização duplicada do Ubuntu foi desabilitada e o horário alinhado ao Windows. Correções menores persistiram; não há prova de estabilidade absoluta nem de que toda contenção veio do relógio. A rodada final confirmou todas as 200 reservas, sem erros de leitura/escrita. Procedimento e reversão no [runbook de qualidade](../runbooks/quality.md). Não foram realizados reset de fábrica, merge automático, deploy, migração histórica, acesso ao MySQL ou criação de recurso pago.

Entrega anterior P01: `a6912886b2155a56a93c12b4b053eef7f6751ea2`. [CI desse commit aprovado](https://github.com/O-marqs/petland-2.0/actions/runs/35990830904), incluindo os jobs `checks` e `browser`. [PR #1 em rascunho](https://github.com/O-marqs/petland-2.0/pull/1), sem merge.

P02: 39 testes Python e 10 React aprovados; Playwright com 11 aprovados e um skip explícito do bootstrap singleton no projeto mobile. Build, tipos, lint, contratos, migrations, auditorias de dependências e atualização Compose aprovados. [Evidências P02, escopo e limitações](../evidence/P02.md); [histórico P01](../evidence/P01.md). O commit desta entrega pode ser localizado com `git log -1 -- docs/implementation/progress.md`; seu CI é registrado nos checks do PR. Revisão/aceite humano não implica merge automático.

## P03 — implementação e verificação

Módulos customers, pets e catalog; migration 0003_catalogs; reutilização pública de autenticação/CSRF/auditoria; API e contratos gerados; área do cliente e da equipe, formulário reutilizado, arquivo/restauração, convite de vínculo e catálogo público. Permissão catalog:manage incluída para EMPLOYEE conforme D07. Gestão de identidades continua ADMIN.

Validado localmente: 55 testes Python (PostgreSQL obrigatório, migrations e concorrência do vínculo), 12 React (incluindo fragmento/StrictMode e versão do formulário), 15 E2E aprovados e um skip explícito do bootstrap singleton no projeto mobile. A jornada da equipe é executada uma vez e inclui viewport de celular. Tipos, lint, build, contratos, acessibilidade automatizada e atualização Compose aprovados. Evidências e limites em [P03](../evidence/P03.md). PR/CI são registrados no próprio PR; não houve merge, deploy ou alteração de main.

## P04 — implementação e verificação

Módulo scheduling, migration 0004_scheduling, coordenação pública com identity/pets/catalog/customers, buffers opcionais por oferta, worker de avisos e contratos gerados. UI em features/booking com configuração, disponibilidade, revisão, detalhe/histórico e comandos. EMPLOYEE recebe establishment:manage conforme D07.

Validação local final: **77 Python + 12 React aprovados**, lint/tipos/arquitetura/contratos/build aprovados. **15 E2E aprovados + um skip explícito do bootstrap mobile**; a jornada ampliada da equipe foi repetida e aprovada após os ajustes finais, incluindo telas de 390/320 px. SMTP real capturado no Mailpit, disputa de vaga e perda de resposta após commit verificados. Compose final saudável; nenhuma falha de Docker. CI e commit exato são registrados no PR, sem merge.

Fontes originais preservadas; alterações do checkout legado intactas. Evidências, caminhos e limites em [P04](../evidence/P04.md); execução em [agenda local](../runbooks/scheduling.md). O commit desta entrega pode ser localizado por `git log -1 -- docs/implementation/progress.md`.

## P05 — implementação e verificação

Execução integrada ao módulo scheduling, migration 0005_operations e contratos gerados. Agenda hoje/semana, detalhe com chegada/início/conclusão/falta, extensão com proteção de pet/pessoa, notas privadas e resumos públicos, histórico filtrado, indicadores e auditoria ADMIN. Configuração protege atendimentos abertos vencidos e permite expediente até meia-noite; identidade/último administrador e comunicação de alterações preservam P02–P04.

Validação final local: **93 Python + 12 React aprovados**, lint/tipos/arquitetura/contratos/build aprovados. **15 E2E aprovados + um skip explícito do bootstrap mobile**, com jornada completa até o histórico, payload privado protegido, gestão, calendário e revogação de acesso. Acessibilidade automatizada e reflow em celular incluídos. Compose saudável; sem problema de Docker. Regras e limites no [ADR-012](../adr/0012-p05-operations.md), [runbook](../runbooks/operations.md) e [evidências P05](../evidence/P05.md).

PR incremental em rascunho sobre P04, sem merge. Resultado remoto e commit exato são registrados no PR. Próximo card PL3-18/P06; publicação continua adiada por D10.

## P06 — implementação e verificação

Segurança, foco/títulos, carregamento acessível, estabilidade visual, agregação/índices e redução de consultas implementados. `python scripts/dev.py check` aprovado: **101 Python + 15 React**, tipos, lint, contratos, arquitetura, migrations e build. Auditorias de dependências aprovadas. Compose final saudável e **15 E2E aprovados + um skip explícito do bootstrap mobile**, incluindo SMTP real, três perfis, jornada até histórico, dados privados, teclado e reflow. Fontes oficiais, main, tag e alterações do checkout legado conferidas e preservadas.

Medição API normal com 100 mil agendamentos e 20 sessões: todas as leituras abaixo de 400 ms no p95 e 200 reservas confirmadas, p95 **775,91 ms** (meta 800 ms). Laboratório web: **9/9 amostras aprovadas**, LCP máximo 2028 ms, INP máximo 88 ms, CLS máximo 0,00119. Metas e timeouts mantidos; resultados e limites de ambiente no [registro P06](../evidence/P06.md). CI repete a carga API em Linux limpo, independentemente do relógio WSL local.

P06 integrada pelo usuário no [PR #6](https://github.com/O-marqs/petland-2.0/pull/6), merge `e90e17a`. [CI do commit `1607cbe` aprovada](https://github.com/O-marqs/petland-2.0/actions/runs/36894412439): checks/browser, carga Linux com reserva p95 427,37 ms e leituras até 215,35 ms, 15 E2E + skip mobile previsto. **Aceite humano com leitor de tela continua pendente**; usuário autorizou explicitamente avançar P07. Ver [roteiro de aceite](../runbooks/quality.md).

## P07 — dados e ensaio operacional local

Demo sintética isolada, transação de seed e UUIDs estáveis, reset preservando origem, servidor estático com TLS, imagem identificável, PostgreSQL verify-full, SMTP STARTTLS, cookies Secure/HttpOnly e proxy sem cache da API. Ferramentas offline recusam produção/bancos fora do namespace e não expõem credenciais. D08/D12 dispensam dados históricos; não declarar migração executada.

Backup custom autenticado/criptografado e restore em banco novo, contagens/digests de todas as tabelas, ACLs e duas exclusões GiST conferidos. Cópia ativada e três perfis verificados no navegador a 320 px, depois retorno à origem. Cadastro/SMTP, capacidade, propriedade, notas privadas e idempotência persistida também verificados na cópia. CI adicionada para repetir o ensaio completo em ambiente limpo.

Verificação final local aprovada: 114 testes Python + 15 React no check completo, 15 E2E + 1 skip mobile previsto, auditorias sem vulnerabilidade conhecida e nove verificações de perfis no staging. Falha de startup do destino restaura o apontamento anterior e tenta reiniciar a origem; cenário de falha verificado em teste. [CI P07 aprovada](https://github.com/O-marqs/petland-2.0/actions/runs/36905134678): checks/browser/operations, 23 tabelas reconciliadas; merge pelo usuário no PR #7 (`3dde06b`). Resultados e limitações em [P07](../evidence/P07.md), reprodução no runbook. Backup continua no mesmo host; retenção/cópia externa, RPO/RTO produtivos e publicação dependem de D10. Fontes, histórico e alterações do legado preservados.

## P08 — candidata e case de revisão

Versões npm/OpenAPI/factory `3.0.0-rc.1` e Python `3.0.0rc1`, contratos regenerados; nenhuma mudança de schema ou regra comercial. Case com problema/decisões/trade-offs/limites, antes histórico isolado do commit preservado, depois real, vídeo integral de 185,12 segundos sem áudio, WebVTT/transcrição, diagramas de contexto/containers/transação e DER/dicionário. Dados/identidades/serviço fictícios e preparação declarada, sem relógio simulado ou senhas filmadas.

Cadastro e reserva UI → chegada/nota privada/início/conclusão UI → histórico público → gestão/impacto/auditoria: mesma reserva conferida na API; nota interna ausente do payload cliente; impacto não altera configuração/reserva. Quatorze checkpoints de captura aprovados. Origens/reset preservados, demonstração retornou ao banco anterior; smoke real novamente aprovado.

Check completo local: 114 Python + 15 React, lint/tipos/contratos/build/migrations/arquitetura/scan. Player verificado a 1280/320 px: duração real, legendas, capítulos, links locais, axe/reflow e ausência de erro JavaScript. O servidor padrão sem ranges não permitia saltar capítulos; preview dedicado fixa loopback/pasta pública e ranges, agora exercitado na CI. `release.py` confere versões/artefatos, empacota árvore Git limpa com hashes/gates e verifica sem extrair; não publica, tagueia ou concede aceite.

Evidências em [P08](../evidence/P08.md), [case](../case/README.md) e [qualidade](../release/quality-report.md). CI/pacote do commit exato ficam registrados no PR. Próximo gate: revisão humana de produto/leitor de tela e decisão D10 antes de release estável/publicação. Candidata não é serviço comercial nem alegação de recuperação após perda do host.

## Correção do primeiro acesso após P08

P08 integrada pelo usuário no PR #8, merge `3fba527`; correção em `petland-3.0-onboarding-fix` com PR incremental sobre P04. [Pedido humano](Onboarding-request.txt): conta recém-cadastrada sem orientação para confirmar e-mail, criar pet e agendar.

Reproduzido: cadastro/SMTP local e login reais funcionavam; faltavam indicação da caixa local, sequência contato/pet/reserva e pré-requisito claro no agendamento. Corrigidos conclusão/foco do cadastro, caixa de e-mails de teste, atualização da confirmação, links para área atual, primeiros passos do dashboard e guarda de contato no agendamento. Segurança/API/schema/agenda mantidos. [Roteiro manual](../runbooks/manual-acceptance.md), [evidência e limites](../evidence/Onboarding.md).

Check completo: 114 Python + 18 React; E2E 15 aprovados + skip mobile previsto. Conta criada pela interface no HTTPS local confirmou mensagem, salvou contato/pet, reservou e conferiu persistência. Funcionário acessou a mesma reserva, reagendou/cancelou; quatro avisos SMTP capturados. Nove checkpoints com axe/reflow aprovados. CI repete a nova jornada de staging; resultado do commit exato registrado no PR. Nenhum aceite humano ou merge automático concedido. Próximo passo: teste pessoal do usuário com cliente/funcionário, mantendo D10 e leitor de tela pendentes.

## Revisão das dores e identidade PetLand

[Pedido posterior](Product-review-request.md): dores, equipe por data, crítica de navegação e visual autoral do PetLand/case. [Matriz](../product/functional-gap-analysis.md) registra cobertura parcial/ausente e decisões vigentes; recursos físicos, lembretes, transferência independente e indicadores por pessoa permanecem lacunas. Sem presumir todos os novos módulos ou alterar D02.

PostgreSQL confirma 5 → 3 → 5 pessoas em dias adjacentes. Formulário carrega a semana da loja ao sair da herança, com orientação de folga/proteção de reservas. [Direção e padrões UX](../ux/visual-review.md): fotografia identificada, composição editorial e jornada numerada; topo para tutor, lateral agrupada para equipe, atalhos/menu acessível em celular. Case recebeu captura com origem; mídia P08 permanece histórica.

Check 115 Python + 18 React; E2E com novo build: 15 aprovados + skip singleton previsto. Staging TLS preservou mesma demo; 16 checkpoints da revisão, onboarding com 4 avisos SMTP e player aprovados. Desempenho final 9/9: LCP 2424 ms, INP 56 ms, CLS 0,0011783. Primeira rodada/falha de classificação do 401 esperado registrada, sem relaxar metas. [Evidência](../evidence/Product-review.md). PR #9 incremental em rascunho sobre P04; checks do commit exato registrados no PR. Próximo gate: revisão humana; escala coletiva/transferência são recomendações para priorização. D10, leitor de tela e aceite final pendentes.

Na CI, corrigidos seletor do título visível no ensaio móvel e período padrão da auditoria (UTC, separado do dia da loja nas métricas). Dois testes de regressão na passagem de data elevam a suite React a 20 aprovados; lint/tipos/build aprovados. Ensaios locais dos três perfis e retorno à área correta passaram. Falhas e correções registradas na evidência; aguardar os checks do commit final antes de declarar a candidata aprovada.

## Evolução operacional autorizada

[Pedido humano](Operations-evolution-request.md) permite implementar prioridades e exercer julgamento de produto. Incremento sobre `18c8945`, separado na branch `petland-3.0-operations-evolution`; PR incremental sobre onboarding-fix, sem merge/main/publicação. [ADR-016](../adr/0016-operational-evolution.md), [matriz](../product/functional-gap-analysis.md), [uso](../runbooks/operational-evolution.md).

Entregues painel diário pessoal/equipe/pendências/carga, escala coletiva por data com impacto, pools físicos com concorrência, transferência independente e histórico, alergias com confirmação atual, contexto de cuidados anteriores, lembrete/aviso de pronto e indicadores por responsável final. Mantidos contrato, privacidade, idempotência, exclusões e D02/D03/D04/D10. Migration 0007 preserva dados e recusa downgrade destrutivo; backup captura revisão real do banco. Case recebe captura separada, preservando vídeo P08.

Check final local: 128 Python + 20 React. E2E 15 aprovados + skip singleton; revisão 16 checkpoints, novos fluxos HTTPS/SMTP reais e reflow/axe. Medições de carga reprovadas motivaram agregações, contagem global separada de pets/clientes e compartilhamento do cálculo de capacidade dentro da consulta. Novos testes preservam exceções individuais/pontuais, recortes e limites de horário de verão. Resultado final/CI do commit exato no PR, sem mascarar as falhas. Web final 9/9, com estilos operacionais carregados junto à área autenticada. [Evidência](../evidence/Operations-evolution.md).

Próximo gate: teste pessoal de tutor/funcionário/gerente, leitor de tela e D10. Reserva em grupo, serviço alterado durante execução, férias por intervalo, lote, recepção em tela única, recorrência e rateio de esforço continuam lacunas explícitas, sem declarar todas as dores concluídas.

## Consolidação documental para portfólio

[Pedido humano integral](Documentation-review-request.txt) autoriza auditar e consolidar o estado atual sem mudar regras/schema, fazer merge ou publicar release. Branch `petland-3.0-portfolio-docs` parte do funcional `2549523`; PR #10 foi integrado em onboarding `d564114`, com conteúdo equivalente. PR #9/main continuam dependências de revisão no snapshot de 02/10/2026; número de PR não cria fases P09/P10.

Criadas visões de produto, UX final em Markdown, arquitetura C4 L1–L3/ports/adapters/DDD pragmático e RNFs com meta/medição/evidência/limite. Modelo de dados, design system, ADRs, matriz, runbook e portal atualizados; README refeito por último. Discovery, PDF original, vídeo P08, capturas e benchmarks anteriores preservados e identificados por referência. Sete páginas Draw.io editáveis/SVG/Mermaid compartilham gerador determinístico. Oito capturas atuais usam somente fixture sintético em `petlanddocs`, isolado dos dados pessoais.

Validação local: 128 Python +20 React; E2E 15 pass +1 skip singleton previsto; captura 16 checkpoints desktop/mobile com axe/reflow/zero erros; 14 Mermaid parseados/renderizados; XML, links/anchors, hashes, pixels lossless, determinismo e release check aprovados. Setup/captura/teardown reproduzidos preservando staging/volumes. Lint inicial do script de captura corrigido e repetido. Nenhum diff funcional/migration/contrato/infra. [Auditoria e resultados](../evidence/Documentation-review.md) registram correções e limites; medições anteriores não são chamadas de novas.

Documentação preparada para revisão humana. Não há pipeline existente seguro/reprodutível de PDF final: Markdown é a fonte atual; PDF discovery permanece íntegro. Aceite dos três perfis/leitor de tela, lacunas funcionais, desempenho Windows/WSL, D10/provedor/SMTP externo/off-host/SLO-RPO-RTO seguem explícitos. Próximo gate é revisão humana do produto e do material, sem merge/publicação automática.

## Auditoria de reprodução e entrega

[Pedido integral](Reproducibility-review-request.txt), recebido sobre `4ef44e0` (PR #11). Branch `petland-3.0-reproducibility` sobre portfolio-docs; mesma candidata/schema/funcional `2549523`. Corrigidos checkout divergente, runbook de release em 0006, identidade com funcionalidades descritas como futuras e roteiro coletivo por data. README revisado por último com cinco caminhos, requisitos host distintos, contas geradas/Mailpit, portas/namespace, preservação e leitura em 30 s/5/10/15+ min. Licença geral ausente registrada, sem adoção automática.

Clone remoto independente sob Documents/GitHub, sem arquivos privados copiados: init/up/migration 0007/live/ready/React/PG/Mailpit, instalação host pelos lockfiles, check **128 Python +20 React**, E2E **15 pass +1 skip singleton** aprovados. Demo nova com CA/contas/volume próprios: init/seed idempotentes, SMTP/TLS, reset, backup/restore/reconciliação, três perfis na origem/cópia/retorno. Ambientes anteriores retomados; staging preservou imagens/ponteiro/contagens. Opção `start --wait` do orquestrador recusada pelo Compose local, corrigida para `start` + health; `dev.py up` aprovado sem alteração.

Ignore e guards das ferramentas reforçados para chaves/bancos/dumps/caches/artefatos, sem mudança no produto. Verificação do pacote compara commit Git no ZIP/manifesto, hashes/inventário e recusa caminhos/duplicatas/segredos conhecidos; **oito testes** aprovados dentro da etapa de CI existente. Links/âncoras/proveniência, diagramas determinísticos, candidata, scan, Ruff/format e React format aprovados. Bundle anterior de 395 arquivos também verificado. [Resultados e limites](../evidence/Reproducibility-review.md), [resumo público sem credenciais](../evidence/Reproducibility-review.json).

CI/clone/pacote do commit desta revisão ficam registrados no PR e no manifesto local, sem conceder aceite humano. Próximas decisões: revisão do material/produto, leitor de tela, licença e D10. Sem merge/tag/release/publicação ou dependências atualizadas.

## Apresentação final do escopo implementado

[Pedido integral](Final-case-request.txt) após merges humanos dos PRs 11/12 em onboarding `f3d70a2`. Branch `petland-3.0-final-case`, base onboarding. Case reescrito em problema/diagnóstico/decisões/arquitetura/experiência/engenharia/resultados/trade-offs/limites, player editorial com Engineering Highlights e README apontando primeiro ao material final. P08 separado como histórico, mídia original preservada; checkout atual/documentação de execução coerentes.

Demo própria `petlandfinalcase`, 8445/55436/8028, sem pausar/copiar staging pessoal. Vídeo contínuo **240,16 s**, sem áudio/cortes/aceleração, **19 capítulos/legendas** e **22 capturas lossless** desktop/mobile. Tutor → reserva confirmada → painel/agenda/contexto/chegada/transferência/início/conclusão → histórico público → indicadores/escala de uma data/capacidade/impacto/auditoria. Persistência/API/SMTP Mailpit/nota privada/versão preservada conferidos, dados fictícios e preparações declarados. Nenhum diff funcional/schema/contrato/infra/dependência contra origem.

Tentativa 1 falhou em mobile: nome longo do pet expandiu detalhe do tutor para 334 px em viewport 320. Tentativa 2 usa Nala e passou; a limitação de texto longo permanece explícita, sem mudança do produto para a gravação. Player final/histórico verificados a 1280/320 px, todos os capítulos/legendas/ranges/links/transcrição/axe/reflow/zero erros JS. [Evidência e arquivos](../evidence/Final-case.md), [origem com hashes](../case/media/final/capture.json).

Checks de documentação/hashes/diagramas/guard de pacote/lint e CI do commit desta revisão registrados na evidência/PR conforme execução; sem aceitar resultado antecipado. Próximos gates: revisão humana do material/produto/leitor de tela, licença e D10. Sem merge/tag/publicação/release estável.


## Higiene do repositório público — 05/10/2026

Branch `chore/public-sanitization`, base main `68dfb35`: neutralizados cinco caminhos pessoais/internos na documentação, sem modificar originais, mídia, funcionalidades ou evidências medidas. Guard atual e novos bundles rejeitam caminhos pessoais, bancos/dumps disfarçados e credenciais legadas conhecidas por fingerprint; pacotes históricos preservam seus caminhos. [Política e bloqueio histórico](../security/public-repository.md).

Gitleaks 8.30.1 no estado atual, histórico alcançável e fonte da Release: três achados atuais e onze históricos, todos falsos positivos revisados (hashes de proveniência e código de dependências). Revisão manual encontrou três credenciais fixas no legado, ausentes no estado atual/pacote v3.0.0: conclusão global BLOCKED até tratar a exposição. Tags, autoria histórica e assets preservados; e-mail noreply configurado somente neste clone. Manifest, checksums e 444 arquivos do ZIP histórico verificados.

Documentação, guard, 21 testes de release/higiene, consistência da release, lint/formatação, mypy, arquitetura, contratos/build e 20 testes React passaram localmente. `dev.py check` chegou à integração e foi impedido pelo Docker indisponível; não declarar integração local aprovada. Resultados da CI do commit exato ficam no PR. Nenhum merge autorizado.
