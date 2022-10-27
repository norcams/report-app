NAME=report-app
VERSION=2.0.0
PACKAGE_VERSION=1
DESCRIPTION="Simple REST API for NREC"
URL="https://github.com/norcams/report-app"
MAINTAINER="https://github.com/norcams"
RELVERSION=8
INSTALL_DIR=/opt/report-app
GIT_REF=master

.PHONY: default
default: deps build rpm
package: rpm

.PHONY: clean
clean:
	rm -fr /installdir
	rm -f $(NAME)-$(VERSION)-*.rpm
	rm -Rf /vendor/

.PHONY: deps
deps:
	dnf module reset ruby -y
	dnf install -y @ruby:2.7
	dnf install -y gcc rpm-build ruby-devel httpd-devel
	gem install -N fpm #--version 1.11.0
	dnf install -y python39 python39-devel python3-virtualenv

.PHONY: build
build:
	mkdir /vendor
	mkdir -p /installdir${INSTALL_DIR}

	cd /vendor; git clone -b ${GIT_REF} ${URL}
	rsync -avh --exclude '.git' /vendor/${NAME}/ /installdir${INSTALL_DIR}
	cd /installdir${INSTALL_DIR}; virtualenv --clear -p /bin/python3.9 .
	#cd /installdir${INSTALL_DIR}; bin/pip install -U setuptools
	cd /installdir${INSTALL_DIR}; bin/pip install -U pip

	#cd /installdir${INSTALL_DIR}; bin/python setup.py install
	cd /installdir${INSTALL_DIR}; bin/pip install --upgrade pip
	cd /installdir${INSTALL_DIR}; bin/pip install -r requirements.txt
	cd /installdir${INSTALL_DIR}; virtualenv --relocatable -p /bin/python3.9 .
	# Hack
	# echo "${INSTALL_DIR}" > /installdir${INSTALL_DIR}/lib/python2.7/site-packages/report_api.egg-link
	# sed -i 's/\/installdir\/opt/\/opt/g' /installdir${INSTALL_DIR}/bin/activate
	# version file
	cd  /vendor/${NAME}; echo "commit: `git log --pretty=format:'%h' -n 1`" > /installdir${INSTALL_DIR}/version.yaml
	echo "version: ${VERSION}" >> /installdir${INSTALL_DIR}/version.yaml
	rm -rf /installdir/usr

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
