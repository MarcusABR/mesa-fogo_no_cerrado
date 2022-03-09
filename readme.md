# Forest Fire Controlled Model

## Resumo

Nesta versão da simulação de incêndios na floresta, são combinados dois métodos de controle para observar o quanto conseguem conservar da área verde original de acordo com as condições do evento. Os dois procedimentos são: A  probabilidade de foco de incêndio ser controlado por bombeiros e apagado antes de se espalhar para a próxima árvore e pela queima intencional de pontos para criar obstáculos ao avanço do fogo.

A propriedade "probability of extinguishment" pode ser alterada por meio da interface, ela altera o valor da variável "ext_prob" no arquigo agent.py. Assim para que o fogo passe para a próxima árvore, o valor padrão é de 50%.

Já a propriedade "burned density", também alterada na interface diz respeito à densidade de árvores que já estarão queimadas no início da simulação. São criados clusters de árvores já queimadas que servem como obstáculos à ploriferação do fogo. Para evitar que grandes clusteres sejam queimados, os valores selecionados devem ser pequenos, uma vez que, para valores muito altos, grande parte da área verde é perdida. No _init_ do models.py, após todas árvores serem instanciadas, os clusteres são criados.

O indíce de sucesso é calculado no modelo na função saved_tress, que retorna a porcentagem das árvores saudáveis em relação às árvores queimadas. Este é salvo nos dados coletados do modelo, juntamente com a "burning density" e extinguish probability" escolhida. Estes dois últimos também estão salvos nos dados coletados do agente, agrupados com o estado de cada árvore. 

Obs: Para evitar conflitos de nomeação no windows, os arquivos seguem o padrão:  _burn_dens_1_ para burning density de 0,1% e _burn_dens_200 para 20%, assim como ext_prob_50 para 50% e _ext_prob_100 para 100%.

## Como usar

Para carregar o modelo com uma interface interativa, use ``mesa runserver`` neste diretório. e.g.

```
    $ mesa runserver
```

Abra o navegador de preferência no link [http://127.0.0.1:8521/](http://127.0.0.1:8521/) pressione Reset, e então Run.



