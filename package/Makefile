NAME=report-app
VERSION=1.0
PACKAGE_VERSION=1
DESCRIPTION=package.description
URL=package.url
MAINTAINER="https://github.com/norcams"
RELVERSION=7

.PHONY: default
default: deps build rpm
package: rpm

.PHONY: clean
clean:
	rm -fr /installdir
	rm -f $(NAME)-$(VERSION)-*.rpm
	rm -Rf /tmp/vendor/

.PHONY: deps
deps:
	yum install -y gcc ruby-devel rpm-build
	gem install -N fpm
	yum install -y python-devel python-virtualenv git libyaml-devel

.PHONY: build
build:
	mkdir /tmp/vendor/
	mkdir -p /installdir/opt/report-app
	cd /tmp/vendor && git clone https://github.com/raykrist/report-app
	cd /tmp/vendor/report-app && git submodule update --init
	rsync -avh --exclude='.git/' /tmp/vendor/report-app/ /installdir/opt/report-app/
	virtualenv /installdir/opt/report-app/
	cd /installdir/opt/report-app/ && bin/pip install -r requirements.txt
	cd /installdir/opt/report-app/ && bin/python setup.py install
	echo "/opt/report-app" > /installdir/opt/report-app/lib/python2.7/site-packages/report_api.egg-link

.PHONY: rpm
rpm:
	/usr/local/bin/fpm -s dir -t rpm \
		-n $(NAME) \
		-v $(VERSION) \
		--iteration "$(PACKAGE_VERSION).el$(RELVERSION)" \
		--description "$(shell cat $(DESCRIPTION))" \
		--url "$(shelpl cat $(URL))" \
		--maintainer "$(MAINTAINER)" \
		-C /installdir/ \
.
