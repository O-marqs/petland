# PetLand 2.0 — Legacy Snapshot

Esta branch preserva a versão anterior do PetLand para fins históricos e comparação com o [PetLand 3.0 na main](https://github.com/O-marqs/petland). O snapshot público foi saneado para remover secrets locais antigos, virtualenv, caches, caminhos gerados e PII ambígua. Código, templates, assets e arquitetura Flask/MySQL permanecem representativos do legado.

- `legacy/petland-2.0`: destino do snapshot público saneado, após merge do PR de saneamento.
- `legacy/petland-2.0-2024-11-24`: tag do snapshot **original**, imutável. Seus commits ainda contêm os valores aposentados e artefatos antigos; o histórico não foi reescrito.
- Este saneamento não altera main, tag ou release `v3.0.0`.

## Reprodução local

Crie uma virtualenv **nova**, instale `pip install -r requirements.txt` e configure no shell as variáveis de `.env.example`. Não há carregamento automático de `.env`. Gere chaves distintas e aleatórias para `FLASK_SECRET_KEY` e `JWT_SECRET_KEY`; `change-me` é somente placeholder. As chaves são obrigatórias e não podem ser vazias. `MYSQL_PASSWORD` é obrigatório ao conectar, com host, usuário e banco configuráveis. Não use as credenciais históricas.

`requirements.txt` foi reconstruído dos imports e metadata de pacotes do snapshot original, sem reutilizar sua virtualenv ou atualizar a arquitetura. `python app.py` mantém o servidor de desenvolvimento Flask em loopback. O esquema/dados MySQL não vieram com o snapshot; não conecte a banco pessoal ou externo para reproduzi-lo. Este legado não é uma aplicação suportada para produção.

## Verificações

```sh
python scripts/check_legacy_snapshot.py
python -m unittest discover -s Tests -p test_legacy_configuration.py
```

Os testes históricos permanecem preservados, inclusive seus imports inconsistentes; não são apresentados como uma suíte verde. Resultados, limitações e inventário em [docs/legacy-sanitization.md](docs/legacy-sanitization.md). O scanner verifica somente arquivos atuais, incluindo adições não ignoradas, e relata identificadores/localizações, nunca valores.
