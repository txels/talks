# Control de Versions?

- Possibilitat de guardar tot l'historial de canvis a un grup d'arxius
- Pots comparar versions en diferents moments
- Pots tornar enrera en el temps

# Tipus de Sistemes:

![Centralitzat](https://homes.cs.washington.edu/~mernst/advice/version-control-fig2.png)


![Descentralitzat](https://homes.cs.washington.edu/~mernst/advice/version-control-fig3.png)


Al sistema descentralizat, tens una còpia completa del repositori (amb tot
l'historial de canvis).

- Pots treballar desconnectat de la xarxa.
- Només necessites connexió per a sincronitzar canvis.

# Operacions bàsiques

- commit: registrar una nova versió (conjunt de canvis)
- push: enviar canvis locals a un servidor remot
- pull: descarregar canvis d'un servidor remot


# git

Avantatges de git

- Descentralitzat
- Molt bona gestió de branques
- Molt eficient


# Utilitzant git - primers passos

Configurar:

    git config --global user.name "John Doe"
    git config --global user.email johndoe@example.com

Necessitarem un repositori. Crear un repo nou:

    git init .

...o clonar un repo existent:

    git clone https://github.com/txels/apitopy.git


# Fent canvis

Si modifiquem arxius localment... què hem canviat?

    git status
    git diff

(diff només ens dirà què ha canviat en arxius que ha estan en control de
versions).

Registrant canvis:

    git add <arxiu[s]>
    git diff --cached
    git commit -m "Missatge..."

Observant canvis registrats:

    git log
    git log --oneline --decorate --graph
    git log --oneline --decorate --graph --all
    git show HEAD

Cada commit té un identificador únic (SHA-256).


# Parèntesi: què vol dir HEAD?

HEAD és una referència (`ref`) que apunta al darrer commit de la branca actual.
(Veurem més en detall branques després).
Per ara saber que hi ha una branca per defecte: `master`.

## Refs

Una referència en git és una mena de "punter" a una versió concreta del
repositori. Altres referències que podem fer servir:

- Noms de branques
- IDs de commits
- Etiquetes (tags)
- Referències relatives, p.e.:
  - `HEAD^` és el commit anterior al darrer.
  - Es pot fer servir també `HEAD^^`, `HEAD~2` etc...
  - `master^`

# Desfent canvis

Desfer el darrer commit:

    git reset HEAD^

Es poden moure i esborrar arxius:

    git mv <nom-original> <nom-nou>
    git rm <nom>

...per registrar els canvis, cal fer commit!


# Parèntesi: index o "staging" area

En git, els canvis es registren en dues "fases":

- stage (add, mv, rm...)
- commit: registrar els canvis amb un missatge (git assigna un ID únic)

Veure què hem canviat:

    git diff  # canvis que no estan a l'index, no es commitegen per defecte
    git diff --cached  # canvis que estan a l'index, es commitejaran

![Cicle d'estats](https://git-scm.com/book/en/v2/images/lifecycle.png)

Si tenim canvis a l'index i els en volem treure, podem fer:

    git reset

Si tenim canvis a l'index i els volem anihilar per sempre, podem fer:

    git reset --hard

(feu-ho només si no us importa perdre aquests canvis)

En alguns casos, es pot fer "add + commit" en una sola comanda:

    git commit -am "Amb xuleria"


# Modificant commits anteriors

També podem modificar un commit existent. Casos típics són que ens hem
descuidat afegir un arxiu, o que volem modificar el missatge. P.e.:

    git commit --amend -m "Un altre missatge"
    git commit -a --amend


# Compartint canvis amb el món

Mentre anem fent i desfent commits, només ens afecta al nostre clon del repo.
Quan estem preparats per publicar els canvis al món, llavors fem:

    git push <remot> <branca>

Si ningú més ha fet canvis a la branca on estem del repo remot, tot anirà bé.

Si hi ha hagut canvis en remot, haurem de fer un `pull` abans de poder fer
`push`. P.e. si estem a `master`:

    git pull origin master
    git push -u origin master


## Parèntesi: què és "origin"?

`origin` és el nom d'un repositori remot. En la convenció de git, el nom
`origin` se li dóna per defecte al repo d'on hem clonat.

Amb git un mateix repo local pot apuntar a molts remots. Quan fem push, hem
d'especificar a quin.


## Parèntesi: github

- Crear compte a github
- Crear repo a github
- Opcional: generar claus RSA?

Pujar el que tenim al repo:

    git remote add origin https://github.com/<usuari>/<repo>.git
    git push -u origin master


# Tags

Podem crear un tag en qualsevol moment per a un commit concret, per a
identificar p.e. una release concreta del nostre porjecte, o qualsevol versió
de referència que ens interessa tenir identificada.

    git tag 1.0.0
    git tag  # llista tots els tags

    git push origin --tags


# Branques

![Branching](https://git-scm.com/book/en/v2/images/branch-and-history.png)

Fem servir branques per aillar millor conjunts de canvis (p.e. si estem
desenvolupant diverses noves funcionalitats alhora, o hem d'arreglar un bug
urgent mentre estem treballant en una nova prestació).

    git branch testing     # crea branca 'testing'
    git checkout testing   # triem 'testing' com a branca activa

En git, una branca és només un punter a un commit determinat. La branca
activa es "mou" quan fem commit.

Quines branques hi ha al repo:

    git branch      # locals
    git branch -a   # locals i remotes

Llegir totes les branques remotes:

    git fetch
    git fetch -p    # esborra branques remotes que ha no existeixen

Podem inspeccionar canvis a la nostra branca respecte de `master`.

    git diff master

O invertint el punt de vista (què hi ha a master re: la nostra branca):

    git diff ..master

Després de fer canvis pertinents (i commit) a la branca, podem en algun
moment incorporar els canvis a la branca `master`:

    git checkout master
    git branch --no-merged
    git merge testing


## Resolució de conflictes

Quan es treballa en dues branques alhora, de vegades en combinar els canvis
es produeixen conflictes.


# Guardar canvis "per més tard"

Podem desar canvis temporalment al "stash":

    git stash
    git stash save "Canvis a mitges de blah..."

Útil si tenim coses a mig editar i hem de canviar de branca, fer pull de
canvis remots etc.



# Aliases

Et pots crear aliases per simplificar les comandes que fas servir habitualment,
o per les que costa recordar.

    git config --global alias.graph 'log --graph --branches --remotes --tags --date-order --oneline --decorate'
    git config --global alias.st status
    git config --global alias.amend 'commit --amend'
    git config --global alias.unstage 'reset HEAD --'
    git config --global alias.last 'log -1 HEAD'
    git config --global alias.visual '!gitk'

(~/.gitconfig)

# Links

- [Pro git - llibre online](https://git-scm.com/book/en/v2)
