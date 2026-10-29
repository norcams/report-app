NAME=report-app
VERSION=2.2.0
PACKAGE_VERSION=1
DESCRIPTION="Simple REST API for NREC"
URL="https://github.com/norcams/report-app"
MAINTAINER="https://github.com/norcams"
RELVERSION=9
INSTALL_DIR=/opt/report-app
GIT_REF=master

.PHONY: default
default: deps build rpm
package: rpm

.PHONY: clean
clean:
	rm -fr /installdir
	rm -fr ${INSTALL_DIR}
	rm -f $(NAME)-$(VERSION)-*.rpm
	rm -Rf /vendor/

.PHONY: deps
deps:
	dnf module reset ruby -y
	dnf install -y @ruby:3.3
	dnf install -y gcc rpm-build ruby-devel python3.12-devel
	gem install -N fpm #--version 1.11.0
	gem install -N json

.PHONY: build
build:
	mkdir /vendor
	mkdir -p ${INSTALL_DIR}

	cd /vendor; git clone -b ${GIT_REF} ${URL}
	rsync -avh --exclude '.git' /vendor/${NAME}/ ${INSTALL_DIR}
	cd ${INSTALL_DIR}; python3.12 -m venv .
	cd ${INSTALL_DIR}; bin/pip install --upgrade pip
	cd ${INSTALL_DIR}; bin/pip install -r requirements.txt
	# version file
	cd  /vendor/${NAME}; echo "commit: `git log --pretty=format:'%h' -n 1`" > ${INSTALL_DIR}/version.yaml
	echo "version: ${VERSION}" >> ${INSTALL_DIR}/version.yaml
	mkdir -p /installdir/opt
	cp -R ${INSTALL_DIR} /installdir/opt/

.PHONY: rpm
rpm:
	/usr/local/bin/fpm -s dir -t rpm \
		-n $(NAME) \
		-v $(VERSION) \
		--iteration "$(PACKAGE_VERSION).el$(RELVERSION)" \
		--description ${DESCRIPTION} \
		--url ${URL} \
		--maintainer ${MAINTAINER} \
		--rpm-tag '%define _build_id_links none' \
		--rpm-tag '%undefine _missing_build_ids_terminate_build' \
		-C /installdir/ \
		.
