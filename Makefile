#!/bin/make

# AUTHOR:  Chris Reid <spikeysnack@gmail.com> #
# LICENSE: Free for all purposes              #
# COPYRIGHT: 2020 - Chris Reid                #


# modification allowed 
# but original attribution stays, add your name to any mods 
# no guarantees implied or inferred
# standard C 
# to build: "just type make"

SHELL = /bin/sh
PY=$(shell which python3)
prefix= $(HOME)
#prefix = /usr/local
bindir = $(prefix)/bin
mandir = $(prefix)/share/man
manext = 7
docdir = $(prefix)/share/doc/nv
srcdir = src
INSTALL = $(shell which install)
INSTALL_PROGRAM = $(INSTALL)

NV.PY := $(bindir)/nv.py

#.PHONY: all  install install-bin install-man install-doc uninstall test



all:	install nv.py

#install:	install-bin  install-man install-doc
install:	$(bindir)/nv.py	install-bin 
	$(PY) -m compileall $(bindir)/nv.py
#	$(MAKE) test

install-bin:	nv.py
	$(INSTALL_PROGRAM) -p  --mode=0755  nv.py $(bindir)/
	ln -sf $(bindir)/nv.py $(bindir)/nv

install-man:	nv.py doc/nv.py.1
	mkdir -p $(mandir)
	$(INSTALL_PROGRAM) --mode=0644 doc/nv.py.1 $(mandir)/man$(manext)/

install-doc:	nv.py
	mkdir -p $(docdir)
	$(INSTALL_PROGRAM) -d -g users --mode=0755 $(docdir)
	cp -a doc/* $(docdir)

reinstall:|	$(NV.PY)
	mv $(bindir)/nv.py  $(bindir)/nv.py.old
	$(MAKE) update
	$(MAKE) install


test:	| $(install)
	@nv test

update:
	@{ GF=$(shell git fetch origin 2>&1); \
	   if [[ "$${GF}" ]]  ; then git merge origin ; \
	   else     echo "nv is already up to date." ; fi }


uninstall:
	rm  -f $(bindir)/nv.py
	rm -rf $(bindir)/__pychache__ 
	rm  -f $(mandir)/nv.py.1 
	rm  -rf $(docdir) 

clean:
	rm -f *~ 
