#!/bin/bash
#
# verificar-atualizacoes.sh: compara os pacotes de home:caiocco com
#   - o projeto de onde foram copiados (copypac), quando conhecido;
#   - o openSUSE:Factory;
#   - a versão mais nova conhecida pelo Repology (upstream).
# Links (linkpac/branch) acompanham a origem sozinhos; para eles só se
# verifica se o link está quebrado ou aponta para um home: de terceiros.
#
# Uso: ./verificar-atualizacoes.sh [-a] [-q] [pacote...]
#   -a  mostra todos os pacotes, não só os que têm novidade
#   -q  não consulta o Repology (mais rápido)
# Sem novidades, não imprime nada (bom para cron, que só manda e-mail
# quando há saída).
#
# Não é um pacote: o osc mostra este arquivo como "?" e o ignora.

PRJ=home:caiocco
REPO=openSUSE_Leap_16.0
ARCH=x86_64
UA='home-caiocco-update-check/1.0'

# Projeto de origem dos pacotes copiados com copypac (pacote=projeto).
declare -A ORIGEM=(
	[antiword]=KDE:Extra
	[recoll]=KDE:Extra
	[unrtf]=KDE:Extra
	# sincronizados com a Factory, mas sem link: o Leap tem ocaml-rpm-macros mais antigo
	[unison]=openSUSE:Factory
	[ocaml-lablgtk3]=openSUSE:Factory
	[zoitechat]=network
	[nx-libs]=home:ithod:x2go
	[x2goserver]=home:ithod:x2go
	[x2goclient]=home:ithod:x2go
	[q4wine]=Emulators
	[lagrange]=openSUSE:Factory
	[harvid]=multimedia:proaudio
	[texstudio]=Publishing
)

# Nome do projeto no Repology, quando difere do pacote ("-" = não consultar).
declare -A REPOLOGY=(
	[dosbox074]=dosbox
	[ocaml-lablgtk3]=ocaml:lablgtk
	[python-Markups]=python:markups
	[python-chunspell]=python:chunspell
	[python-python-markdown-math]=python:python-markdown-math
	[rox-filer2]=rox-filer
	[skeuos-gtk]=-
	[orbitiny-desktop]=-
	[leibnitz]=-
	[system-g]=-
	[jx-ide]=-
	[hackneyed]=-
	# cada distribuição usa um esquema de versão diferente (1.0.2, 2.23.1, 3066...)
	[treesheets]=-
	# é o fork NEdit Classic (alx210/nedit-classic); o "nedit" do Repology é o original
	[nedit]=-
	# snapshots do macemu (kanjitalk755); cada distro versiona de um jeito
	[BasiliskII]=-
	[SheepShaver]=-
	# upstream morto (última versão 8.0.2, 2008)
	[bluecurve-cursor-theme]=-
)

# Pacotes que não devem ser comparados com o homônimo da Factory.
declare -A SEM_FACTORY=(
	[nedit]=1   # a Factory tem o NEdit original, não o fork NEdit Classic
)

# Versões exatas a desconsiderar (falsos positivos), separadas por espaço.
# Valem para origem, Factory e Repology; uma versão nova de verdade ainda aparece.
declare -A IGNORAR=(
	# o Repology mistura o Surge antigo (1.9.0, Nix/Homebrew) com o Surge XT
	[surge-xt]="1.9.0"
	# FreeBSD numera o snapshot pelo nº de commits; o nosso já é o último commit
	[chicago95]="3.0.1.49"
	# revisão de pacote (opam), não versão nova do upstream
	[ocaml-lablgtk3]="3.1.5-1"
	# snapshot da Factory (2024) é mais velho que a tag 1.3.0-alpha.2 (2026-09);
	# o rpm acha ~git > ~alpha
	[lmms]="1.3.0~git2024.09.21"
	# ebuild "live" do Gentoo (git master)
	[yggdrasil-go]="9999"
)

ignorado() { # pacote versão
	[[ " ${IGNORAR[$1]} " == *" $2 "* ]]
}

mostrar_tudo=0
sem_repology=0
while getopts aq opt; do
	case $opt in
		a) mostrar_tudo=1 ;;
		q) sem_repology=1 ;;
		*) sed -n '9,12p' "$0"; exit 2 ;;
	esac
done
shift $((OPTIND - 1))

# vercmp A B: imprime 1 se A > B, 0 se iguais, -1 se A < B
# (ignora ".0" no fim, para que 0.74.3.0 seja igual a 0.74.3)
vercmp() {
	local a=$1 b=$2
	while [[ $a == *.0 ]]; do a=${a%.0}; done
	while [[ $b == *.0 ]]; do b=${b%.0}; done
	rpm --eval "%{lua: print(rpm.vercmp('$a', '$b'))}"
}

# versão do src.rpm publicado de um pacote; vazio se não houver
versao_binaria() { # projeto pacote repositório
	local src
	src=$(osc ls -b "$1" "$2" -r "$3" -a $ARCH 2>/dev/null | grep -m1 '\.src\.rpm$') || return
	src=${src%.src.rpm}
	src=${src%-*}             # tira o release
	echo "${src##*-}"         # tira o nome
}

versao_spec() { # projeto pacote
	osc cat "$1" "$2" "$2.spec" 2>/dev/null | awk '/^Version:/{print $2; exit}'
}

# imprime a versão mais nova; "ERRO" se a consulta falhar duas vezes
versao_repology() { # nome pacote
	local json vs v max= tentativa
	for tentativa in 1 2; do
		json=$(curl -sf --max-time 30 -A "$UA" "https://repology.org/api/v1/project/$1")
		local ok=$?
		sleep 1.1   # o Repology pede no máximo 1 consulta por segundo
		[ $ok = 0 ] && break
		sleep 10
	done
	if [ $ok != 0 ]; then echo ERRO; return; fi
	vs=$(jq -r '.[] | select(.status=="newest" or .status=="unique") | .version' <<<"$json" | sort -u)
	for v in $vs; do
		ignorado "$2" "$v" && continue
		if [ -z "$max" ] || [ "$(vercmp "$v" "$max")" = 1 ]; then max=$v; fi
	done
	echo "$max"
}

if [ $# -gt 0 ]; then
	pacotes="$*"
else
	pacotes=$(osc ls $PRJ | grep -v ':')   # sem os flavors de multibuild
fi

for p in $pacotes; do
	info=$(osc api "/source/$PRJ/$p" 2>/dev/null)
	alvo=$(grep -o 'linkinfo project="[^"]*"' <<<"$info" | cut -d'"' -f2)

	if [ -n "$alvo" ]; then
		aviso=
		if ! osc api "/source/$PRJ/$p?expand=1" >/dev/null 2>&1; then
			aviso="LINK QUEBRADO"
		elif [[ $alvo == home:* ]]; then
			aviso="link para home de terceiros"
		fi
		if [ -n "$aviso" ] || [ $mostrar_tudo = 1 ]; then
			printf '%-28s link -> %-28s %s\n' "$p" "$alvo" "$aviso"
		fi
		continue
	fi

	nossa=$(versao_binaria $PRJ "$p" $REPO)
	[ -z "$nossa" ] && nossa=$(versao_spec $PRJ "$p")
	novidades=()

	if [ -n "${ORIGEM[$p]}" ]; then
		v=$(versao_spec "${ORIGEM[$p]}" "$p")
		if [ -n "$v" ] && ! ignorado "$p" "$v" && [ "$(vercmp "$v" "$nossa")" = 1 ]; then
			novidades+=("origem(${ORIGEM[$p]})=$v")
		fi
	fi

	v=
	[ -z "${SEM_FACTORY[$p]}" ] && v=$(versao_binaria openSUSE:Factory "$p" standard)
	if [ -n "$v" ] && ! ignorado "$p" "$v" && [ "$(vercmp "$v" "$nossa")" = 1 ]; then
		novidades+=("factory=$v")
	fi

	nome=${REPOLOGY[$p]:-$p}
	if [ $sem_repology = 0 ] && [ "$nome" != - ]; then
		v=$(versao_repology "$nome" "$p")
		if [ "$v" = ERRO ]; then
			novidades+=("repology=falhou")
		elif [ -n "$v" ] && ! ignorado "$p" "$v" && [ "$(vercmp "$v" "$nossa")" = 1 ]; then
			novidades+=("upstream=$v")
		fi
	fi

	if [ ${#novidades[@]} -gt 0 ] || [ $mostrar_tudo = 1 ]; then
		printf '%-28s %-28s %s\n' "$p" "${nossa:-?}" "${novidades[*]:-em dia}"
	fi
done
