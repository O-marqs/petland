# Versão, execução e reprodução

**CURRENT · `main` · release de portfólio `3.0.0` · schema `0007_product_operations`.** Esta página é a referência de checkout/ambiente. [Produto](../product/product-overview.md), [UX](../ux/PetLand_3.0_UX_Final.md) e [arquitetura](../architecture/overview.md) descrevem o código funcional; discovery, capturas e benchmarks conservam suas referências originais.

## Qual versão clonar

**Atual:** clone padrão de `O-marqs/petland`, branch `main`, versão `3.0.0`. PetLand 2.0 está em `legacy/petland-2.0`, exatamente `3cc3f898cde896b80fed587bf8c06f4aa46742f6`. PR #13 integrado por merge commit `968a1451beaa2587764a97d1d257adf597223dff`, preservando PRs 10–12. [Vídeo/capturas finais](../case/README.md) foram gravados em `f3d70a2cce07d587351eadaa66864b7c1ae4444a`, ainda RC: [proveniência original](../case/media/final/capture.json). A promoção de versão não altera regras nem redata essa mídia.

A tabela abaixo preserva o snapshot recebido na auditoria anterior, antes desses merges. Os estados dos PRs nessa tabela são históricos.

| Referência auditada em 02/10/2026                                         | Estado                                                                                                                                                    |
| ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `main` / `3cc3f8`                                                         | Legado PetLand 2.0; não é o checkout do 3.0.                                                                                                              |
| `petland-3.0-onboarding-fix` / `d564114`                                  | PR #10 integrado; código funcional equivalente a `2549523`, sem a consolidação documental posterior. PR #9 ainda em revisão.                              |
| `petland-3.0-portfolio-docs` / `4ef44e03ce4601b753767bfe65fee1d55283f7be` | HEAD mais completo recebido nesta auditoria; PR #11 em rascunho, CI aprovada.                                                                             |
| `petland-3.0-reproducibility`                                             | Incremento desta auditoria sobre `4ef44e0`: instruções de execução e proteção dos artefatos. Branch auditada anteriormente; não concede merge ou release. |

```sh
git clone https://github.com/O-marqs/petland.git
cd petland
git rev-parse HEAD
```

No Windows, coloque o clone em `%USERPROFILE%\Documents\GitHub` ou no diretório equivalente escolhido pelo leitor. Registre o SHA emitido; branches podem avançar. Para repetir um artefato específico, use o SHA do seu manifesto: `git checkout --detach SHA_DO_COMMIT`. A tag anotada `v3.0.0` identifica o commit final validado; não inferir o SHA de mídias antigas pela versão atual.

## Cinco caminhos, requisitos distintos

| Objetivo              | Requisitos no host                                           | Caminho                                                                                 |
| --------------------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| RUN THE APP           | Git, Python 3.11+, Docker com Compose v2 ativo               | `init` → `up`; aplicação vazia e configuração comercial explícita.                      |
| DEVELOP LOCALLY       | Requisitos acima + uv 0.12.18, Node 22.14–22.x, pnpm 10.34.5 | `init` → `install` → `db` → `migrate` → `api` e `web` em terminais separados.           |
| RUN TESTS             | Ferramentas host + Docker                                    | `init` → `install` → `check`; E2E exige `up` e depois `e2e`.                            |
| RUN DEMO              | Git, Python 3.11+, Docker + uv 0.12.18                       | `staging-init` → `staging-up` → `seed-demo`; contas fictícias/expediente já preparados. |
| RUN STAGING REHEARSAL | Ferramentas host completas + Chromium Playwright             | Demo preparada → `smoke-demo` → `rehearse`; backup/restore e três perfis.               |

Imagens precisam de acesso a Docker Hub/GHCR, npm e PyPI na primeira construção; instalação host usa os mesmos registries/lockfiles. Cache existente pode ser reutilizado, sem obrigação de apagar imagens/volumes. Tempo de download/construção depende do host e da rede; “10 minutos” é uma trilha de leitura/execução, não um SLA de instalação.

Python da aplicação é **3.13** (`.python-version`, `pyproject.toml`, imagem e CI); o launcher `dev.py` suporta **3.11+**. uv obtém o Python de projeto quando necessário. Node é **linha 22, mínimo 22.14**; pnpm **10.34.5** está em `packageManager`, Dockerfiles e CI. PostgreSQL é **17**, imagem fixada por digest; patch observado consta na evidência do ensaio. Metadata Python/npm/OpenAPI atual usa **3.0.0**. A RC permanece somente em evidências e ferramentas de captura históricas.

Para instalar ferramentas host, use os instaladores oficiais de [uv](https://docs.astral.sh/uv/getting-started/installation/) e [Node](https://nodejs.org/en/download). Com Node/npm disponíveis, `npm install --global pnpm@10.34.5`; confira `uv --version`, `node --version` e `pnpm --version`. Se outra versão de pnpm estiver no PATH, use uma instalação isolada da versão exigida; não regrave o lockfile com ela. O modo RUN THE APP não exige uv/Node/pnpm no host.

Exemplo de instalação isolada de pnpm na raiz do clone, sem mudar a versão global (PowerShell):

```powershell
npm install --prefix .tools pnpm@10.34.5
$env:PATH = "$((Get-Location).Path)\.tools\node_modules\.bin;$env:PATH"
pnpm --version
```

Essa ferramenta é baixada do npm, não copiada do autor; `.tools` é ignorada. Repita o ajuste de PATH em cada terminal host que precise dela. Para uv, o instalador oficial aceita versão na URL (`https://astral.sh/uv/0.12.18/install.ps1` no Windows, `https://astral.sh/uv/0.12.18/install.sh` no POSIX); siga as instruções oficiais e valide a versão. Não é necessário atualizar ferramentas globais já compatíveis.

## Isolamento e portas

| Ambiente padrão            | Web / API                                     | PostgreSQL                 | E-mails                        |
| -------------------------- | --------------------------------------------- | -------------------------- | ------------------------------ |
| Desenvolvimento `petland3` | http://localhost:5173 / http://localhost:8000 | 55432; teste efêmero 55433 | UI 8025; SMTP 1025             |
| Demo/staging `petland7`    | https://localhost:8443; API interna           | 55434, TLS                 | UI 8026; SMTP interno STARTTLS |

Portas são de loopback e estão fixadas no Compose; somente uma instalação de cada ambiente pode ocupá-las no host. Não executar Vite/API host e os respectivos containers simultaneamente.

Clones diferentes com o mesmo nome Compose compartilham a identidade de projeto/volume. Para um ensaio em clone novo, use nomes próprios **antes do primeiro comando** e libere apenas as portas do ambiente conhecido, preservando seus volumes. Override nativo de Compose, não modificação de arquivo:

```powershell
# PowerShell, clone de ensaio, somente após liberar as portas de desenvolvimento:
$env:COMPOSE_PROJECT_NAME = 'petland-clean-app'
python scripts/dev.py init
python scripts/dev.py up
python scripts/dev.py down
Remove-Item Env:COMPOSE_PROJECT_NAME
```

Para demo use outro nome, por exemplo `petland-clean-stage`, com a mesma variável durante **todos** os comandos de staging, seed, smoke, rehearsal e down. Shell POSIX: `export COMPOSE_PROJECT_NAME=petland-clean-stage`; ao terminar, `unset COMPOSE_PROJECT_NAME`. Isso separa volumes/projetos, mas não muda portas. Não copiar `.env`, `.local/staging`, senhas, CA ou banco de outra instalação. Não usar `down --volumes` para liberar portas.

## Demo para conhecer o produto

```sh
python scripts/dev.py staging-init
python scripts/dev.py staging-up
python scripts/dev.py seed-demo
```

Abra https://localhost:8443/entrar. A CA é local: aceite apenas esse localhost no perfil de teste ou importe somente o certificado público `.local/staging/certs/ca.crt`; não compartilhar chaves. E-mails ficam em http://localhost:8026, sem entrega externa.

Consulte localmente `.local/staging/accounts.json`: `customer_a`/`customer_b` são tutores, `employee` funcionário e `admin` administrador. Todas as senhas são geradas, sem default versionado. Tutor entra em `/app`, equipe em `/operacao`, admin em `/gestao` e `/gestao/acessos`. [Roteiro pessoal](../runbooks/manual-acceptance.md).

`seed-demo` não duplica nem atualiza datas de um fixture já existente. Para um banco novo, `seed-demo --reference-date YYYY-MM-DD` fixa a referência. Se ele envelhecer, leia o nome em `.local/staging/active-db.txt` e use `reset-demo --confirm NOME_EXATO_DO_BANCO`; cria e ativa outro banco, preservando o anterior. Não remover marcador/volume para forçar seed. [Operação/recuperação](../runbooks/operations-recovery.md).

Parar: `staging-down`. Retomar: `staging-up`. Volumes, credenciais, certificados, bancos e backups são preservados. `down` da aplicação e `staging-down` são comandos distintos; banco de teste em tmpfs é descartável.

## Verificar sem confundir os ambientes

```sh
python scripts/dev.py install
python scripts/dev.py check
python scripts/check_documentation.py
python scripts/render_architecture.py --check
python -m unittest discover -s scripts -p test_release.py
python scripts/release.py check
```

Antes de `check`, execute `init`; testes exigem Docker e porta 55433 livre. E2E: aplicativo de desenvolvimento isolado iniciado por `up`, então `e2e`. Ele cria contas/cadastros/reservas sintéticos e exerce o primeiro admin; não rodar contra banco pessoal/produção. Admin preexistente requer as variáveis de fixture descritas no [guia de identidade](../runbooks/identity.md).

Para o rehearsal, execute `install`, prepare a demo e instale `pnpm --filter @petland/web exec playwright install chromium`. Em Linux, bibliotecas do navegador podem exigir `install --with-deps chromium`. Execute `smoke-demo` antes de `rehearse`; relatório privado em `.local/staging/rehearsal.json`. A origem volta a ficar ativa após validar a cópia. Não é recuperação após perda do host nem aceite humano.

## Pacote e licença

[Release local](../runbooks/release.md): `bundle` exige commit/árvore limpa; ZIP do Git contém documentação, diagramas, case e mídias. Manifesto registra commit, inventário, SHA-256 e gates; `verify` também compara o commit embutido pelo Git e recusa entradas duplicadas, caminhos privados, bancos/chaves/caches e assinaturas de segredo conhecidas. Não extrai ou publica.

ZIP não inclui `.git` nem dependências/configurações geradas: staging e reprodução histórica requerem clone Git. Hashes/inventário detectam alteração relativa ao manifesto confiável; não substituem assinatura externa, revisão de PII ou auditoria de todo o histórico.

**Licença geral ausente.** Notices de terceiros existentes não licenciam todo o PetLand. Recomendação para o autor: [MIT](https://opensource.org/license/mit) se deseja reuso amplo com preservação do aviso de copyright/licença; considerar [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) se deseja concessão explícita de patentes e suas condições. Nenhuma foi adicionada sem decisão humana.

[Evidência do clean-start e limites](../evidence/Reproducibility-review.md). Essa auditoria anterior é histórica. O [fechamento autorizado](../evidence/Portfolio-closure.md) promove o portfólio por PR, tag e GitHub Release; aceite humano/leitor de tela e D10 não foram convertidos em aprovação comercial.
