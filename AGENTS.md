# PetLand 3.0 — referência operacional

## Objetivo e fontes

Uma loja, demonstração de portfólio, três perfis. Leia `docs/implementation/progress.md` antes de trabalhar; não recrie entregas concluídas. Fonte primária do estado implementado: código executável, migrations, OpenAPI e testes. Entrada documental atual: `docs/product/product-overview.md`, `docs/ux/PetLand_3.0_UX_Final.md`, `docs/architecture/overview.md` e `docs/README.md`. Plano consolidado e Caderno UX PDF são discovery original: preserve íntegros. Autorizações de fases/incrementos em `docs/implementation`; decisões em `docs/product/decisions.md` e `docs/adr/README.md`.

## Arquitetura e código

- `apps/api`: FastAPI, Python tipado, SQLAlchemy síncrono/psycopg e Alembic; monólito modular hexagonal pragmático.
- `modules/<dominio>/domain`: Python puro; sem FastAPI, SQLAlchemy, Pydantic HTTP ou infraestrutura.
- `application`: casos de uso/autorização contextual e ports pequenas; sem SQL, HTTP ou adapters concretos.
- `infrastructure`: ORM, persistência e integrações; `presentation`: schemas/HTTP; `bootstrap` compõe tudo.
- Módulos não acessam internals alheios; colaborações por contratos públicos. Não adicionar repositório genérico, camada vazia ou abstração sem uso.
- `apps/web`: React/TS/Vite, funcionalidades em `features`, UI em `shared`, composição em `app`. UI não importa features. Dados remotos com TanStack Query, formulários RHF/Zod.
- Tokens em `shared/styles/tokens.css`; fontes locais, pt-BR na interface e contratos técnicos em inglês.
- `packages/api-contract`: OpenAPI/tipos gerados. Nunca editar arquivos gerados manualmente; `pnpm contracts:generate`, depois `pnpm contracts:check`.
- `infra` é local; `docs` guarda decisões e evidências; `scripts/dev.py` centraliza comandos.

## Execução e verificações

Da raiz: `python scripts/dev.py init`, `install`, `db`, `migrate`, `api` e `web` (terminais separados). Alternativa somente Docker: `init` e `up`. Parar com `down`, preservando volume.

Antes de entregar: `python scripts/dev.py check`; aplicação iniciada: `python scripts/dev.py e2e`. Testes de banco só com PostgreSQL efêmero, `APP_ENV=test`, nome terminando `_test`. CI exige integração, sem skip silencioso. Não usar SQLite para regras de PostgreSQL. Execute testes comportamentais proporcionais; não espelhe implementação nem esconda falhas. Não declarar aprovação sem execução.

## Segurança e histórico

- Não copiar credenciais/PII do legado, não acessar MySQL ou migrar dados reais sem autorização específica.
- `.env`, caches, venvs e node_modules nunca versionados. Use configuração validada, logs por allowlist e erros públicos seguros.
- Identidade/permissões sempre no servidor; não guardar tokens em localStorage nem usar CPF como identidade pública. Sessão/CSRF, convites e papéis são implementados em `identity`; não substituir por autenticação simulada. A matriz D07 está em `docs/architecture/authorization.md`.
- Nenhuma reserva fictícia para demonstrar contratos; dados sintéticos somente identificados em demo/testes.
- Preserve tag `legacy/petland-2.0-2024-11-24` e histórico. Não force push, não reescreva história, não altere main, não descarte mudanças alheias. Repositórios locais ficam em `%USERPROFILE%\Documents\GitHub`.
- O worktree `petland-3.0` depende da pasta original `petland 2.0` para os metadados Git; não mova/remova a original.
- Não fazer merge automático, deploy de produção ou criar recursos pagos. PRs de revisão estão autorizados. P06 parte do merge `679eae5` em `petland-3.0-p06`, com base de PR `petland-3.0-p04`, onde P05 foi integrada pelo usuário.

## Conclusão e continuidade

Respeite roadmap/gates. Decisões D01–D11 e recomendações complementares aprovadas no pedido P03; P04 autorizada em P04-request.txt. Leia docs/product/decisions.md e ADR-003 antes de alterar agenda. Estabelecimento é sempre o primeiro lock em mutações críticas; não retirar exclusões de recurso/pet nem idempotência. Agenda começa desabilitada, sem horários/funcionários comerciais. P05 implementa a operação; leia também ADR-012. P06 está autorizada e revisa qualidade, segurança, desempenho e UX; não iniciar P07 automaticamente. Não alterar decisões aprovadas silenciosamente. Registre escopo, RF/RNF, arquivos, implementação, verificações reais, limitações e próximo card em `docs/implementation/progress.md` e `docs/evidence`. Atualize README/runbooks junto ao código. UI isolada não conclui funcionalidade de negócio.

P07 expressamente autorizada após merge P06 `e90e17a`; trabalho em `petland-3.0-p07`, base do PR `petland-3.0-p04`. Leia `P07-request.txt`, ADR-014 e runbook operations-recovery antes de alterar ferramentas offline. A autorização de avanço prevalece sobre a orientação anterior de não iniciar P07 automaticamente. Aceite humano com leitor de tela permanece pendente; não inventar aprovação. D08/D12 dispensam importação histórica; D10 adia publicação/provedor externo. Demo somente em namespace/banco/volume isolados, nunca semear desenvolvimento ou produção. Reset/restore não sobrescrevem origem; ativar cópia somente após reconciliação. Não imprimir/versionar senhas, chaves, tokens ou dump em claro. P08 não começa automaticamente.

Em caso de problema de Docker, a orientação inicial era parar e informar o ajuste. O usuário posteriormente autorizou expressamente a recuperação local do Docker/WSL e o reinício do computador para retomar o trabalho. Essa autorização prevalece: diagnosticar e recuperar os serviços preservando volumes, imagens e dados; não fazer reset de fábrica ou apagar dados.

P08 expressamente autorizada após merge P07 `3dde06b`; branch `petland-3.0-p08`, base do PR P04. Autorização prevalece sobre a orientação anterior de não começar P08 automaticamente. Candidata 3.0.0-rc.1 para revisão, conforme ADR-015: ler case, candidate.json e runbook release. Preservar proveniência histórica e distinguir template isolado de fluxo legado; depois/vídeo somente da aplicação real com dados fictícios identificados. Preview serve só pasta pública no loopback; não expor raiz/.local. Ferramentas de release não concedem aceite. Gates humano final/leitor de tela e D10 permanecem pendentes, sem tag/release estável/publicação automática ou expansão de escopo presumida.

Revisão pós-P08 autorizada em `docs/implementation/Product-review-request.md`: matriz funcional e visual autoral do PetLand/case. Leia `docs/product/functional-gap-analysis.md`, `docs/ux/visual-review.md` e evidência Product-review antes de continuar. Lacunas são propostas, não novos módulos automaticamente autorizados; D02/D03/D10 mantidos. Capacidade por data 5/3/5 verificada; formulário próprio copia a semana da loja ao sair da herança. Tutor usa topo/equipe lateral, com atalhos/menu acessível em celular. Preserve mídia P08; nova capa tem hashes/origem separados. Benchmark distingue apenas GET auth/me 401 esperado de visitante, sem relaxar metas/ignorar outros erros. PR #9 reúne onboarding e revisão; humano/main/publicação continuam gates.

Autorização posterior em `docs/implementation/Operations-evolution-request.md` permite implementar as lacunas prioritárias e dar vida ao backoffice. A autorização prevalece sobre a restrição anterior de somente diagnosticar lacunas. Branch `petland-3.0-operations-evolution` parte de `18c8945`; preserve D02/D03/D04/D10 e os dados. Dashboard deve usar dados reais; relatórios explicitam recorte/atribuição, comunicação não confunde SMTP aceito com entrega externa.

Revisão documental autorizada em `docs/implementation/Documentation-review-request.txt`, sobre código funcional `2549523`; PR #10 integrado em onboarding `d564114`, conteúdo equivalente, main legada/PR #9 ainda pendentes no snapshot de 02/10. Branch `petland-3.0-portfolio-docs`: produto/UX/arquitetura/RNFs/índices/diagramas/capturas atuais, sem mudar regra/schema, merge ou publicar release. Preserve originais/história/medições; não invente P09/P10 a partir de números de PR. Capturas usam projeto/banco sintético separado `petlanddocs`; staging pessoal pode conter dados do autor. `python scripts/check_documentation.py` e `render_architecture.py --check` validam referências/proveniência/exportações; Mermaid atual compartilha fonte com Draw.io/SVG. Leitor de tela/aceite e D10 continuam pendentes.

Auditoria de reprodução autorizada em `docs/implementation/Reproducibility-review-request.txt`, sobre `4ef44e0` (PR #11). Branch `petland-3.0-reproducibility`, base portfolio-docs: somente documentação/configuração e guards das ferramentas de revisão; sem funcionalidade, dependência, schema/contrato, merge/tag/publicação. Fonte de checkout/requisitos em `docs/release/reproducibility.md`, resultados em `docs/evidence/Reproducibility-review.md`. Ensaios independentes usam `COMPOSE_PROJECT_NAME` próprio e arquivos novos; portas fixas exigem pausa/retomada do ambiente anterior, preservando dados/volumes/imagens. Não copiar credenciais ou apagar caches para chamar o teste de limpo. Licença geral ausente: recomendar, sem adotar automaticamente. CI e bundle devem corresponder ao commit declarado.

Apresentação final autorizada em `docs/implementation/Final-case-request.txt`, após merges humanos dos PRs 11/12 em onboarding `f3d70a2`. Branch `petland-3.0-final-case`, base onboarding: case, vídeo/legendas/transcrição/capturas atuais e proveniência, sem mudar regras/features/dependências/schema/contrato/infra ou simular comportamento. Capture somente namespace sintético próprio `petlandfinalcase` (8445/55436/8028), preservando staging pessoal; ferramentas recusam diferença funcional contra o SHA declarado. Mídia final em `docs/case/media/final`; P03–P08 intactos e player P08 histórico separado. `check_final_case.py`, documentação/release e player validam hashes/links/ranges/seek/legendas/reflow/axe. Transbordamento de nome longo a 320 px encontrado na captura fica como limitação registrada, sem alteração do produto nesta revisão. Leitor de tela/aceite/D10/licença continuam pendentes. Sem merge/tag/release/publicação.

## Fechamento autorizado — 02/10/2026

O pedido explícito em `docs/implementation/Portfolio-closure-request.txt` prevalece sobre restrições anteriores de não integrar main, fazer merge/tag/release ou renomear o repositório. Autoriza: merge commit do PR #13 com CI exata verde, preservar legado 3cc3f898, promover metadata 3.0.0 por PR temporário de release com CI verde, renomear para O-marqs/petland, clean clone independente, tag anotada v3.0.0 no main validado, GitHub Release de portfólio/demo, comentar/fechar PRs obsoletos e remover somente branches integralmente alcançáveis por main/tag. Não autoriza features/regras/migrations/arquitetura novas, force push, perda de commits, alterações de evidências históricas, licença automática ou declaração comercial. production_ready permanece false; leitor de tela e D10 pendentes. Publicação é comprovada pela GitHub Release e publication.json anexado após published_at real, mantendo main/tag imutáveis no mesmo SHA.

## Higiene pública autorizada — 05/10/2026

Branch `chore/public-sanitization` parte da main atualizada. Somente auditoria de privacidade/credenciais, neutralização de caminhos e guard com testes; não é fase de produto. Não fazer merge, alterar funcionalidades/arquitetura/regras, reescrever histórico ou mover tags/assets históricos. Qualquer REAL SECRET bloqueia a conclusão global; relatar sem valores e preservar evidências. Política e exposição legada em [public-repository](docs/security/public-repository.md). Configuração noreply pertence apenas ao clone local.
