NAME=report-app
VERSION=1.0
PACKAGE_VERSION=2
DESCRIPTION="Simple REST API for himlar"
URL="https://github.com/norcams/report-api"
MAINTAINER="https://github.com/norcams"
RELVERSION=7
INSTALL_DIR=/opt/report-app

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
	yum install -y gcc ruby-devel rpm-build
	gem install -N fpm
	yum install -y python-devel python-virtualenv git libyaml-devel

.PHONY: build
build:
	mkdir /vendor
	mkdir -p /installdir${INSTALL_DIR}

	cd /vendor; git clone ${URL}
	rsync -avh --exclude '.git' /vendor/himlarservice/ /installdir${INSTALL_DIR}
	cd /installdir${INSTALL_DIR}; virtualenv --clear .
	cd /installdir${INSTALL_DIR}; bin/python setup.py install
	cd /installdir${INSTALL_DIR}; bin/pip install -r requirements.txt
	cd /installdir${INSTALL_DIR}; virtualenv --relocatable .
	# Hack
	echo "/opt/report-app" > /tmp/installdir/opt/report-app/lib/python2.7/site-packages/report_api.egg-link

.PHONY: rpm
rpm:
	/usr/local/bin/fpm -s dir -t rpm \
		-n $(NAME) \
		-v $(VERSION) \
		--iteration "$(PACKAGE_VERSION).el$(RELVERSION)" \
		--description ${DESCRIPTION} \
		--url ${URL} \
		--maintainer ${MAINTAINER} \
		-C /installdir/ \
		.
