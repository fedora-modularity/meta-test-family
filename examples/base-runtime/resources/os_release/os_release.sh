#!/bin/bash
set -e  # exit immediately on any failure

. /etc/os-release

EXP_NAME="Fedora Modular"
EXP_VERSION="26 (Twenty Six)"
EXP_ID="fedora-modular"
EXP_ID_LIKE="fedora"
EXP_VERSION_ID="26"
EXP_PRETTY_NAME="Fedora Modular 26 (Twenty Six)"
EXP_ANSI_COLOR="0;34"
EXP_CPE_NAME="cpe:/o:fedoraproject:fedora-modular:26"
EXP_HOME_URL="https://fedoraproject.org/"
EXP_BUG_REPORT_URL="https://bugzilla.redhat.com/"
EXP_REDHAT_BUGZILLA_PRODUCT="Fedora"
EXP_REDHAT_BUGZILLA_PRODUCT_VERSION="26"
EXP_REDHAT_SUPPORT_PRODUCT="Fedora"
EXP_REDHAT_SUPPORT_PRODUCT_VERSION="26"
EXP_PRIVACY_POLICY_URL="https://fedoraproject.org/wiki/Legal:PrivacyPolicy"

if [[ $NAME != $EXP_NAME ]]; then
    echo "FAIL: Expected NAME to be '$EXP_NAME', but it is '$NAME'"
    exit 1
fi

if [[ $VERSION != $EXP_VERSION ]]; then
    echo "FAIL: Expected VERSION to be '$EXP_VERSION', but it is '$VERSION'"
    exit 1
fi

if [[ $ID != $EXP_ID ]]; then
    echo "FAIL: Expected ID to be '$EXP_ID', but it is '$ID'"
    exit 1
fi

if [[ $ID_LIKE != $EXP_ID_LIKE ]]; then
    echo "FAIL: Expected ID_LIKE to be '$EXP_ID_LIKE', but it is '$ID_LIKE'"
    exit 1
fi

if [[ $VERSION_ID != $EXP_VERSION_ID ]]; then
    echo "FAIL: Expected VERSION_ID to be '$EXP_VERSION_ID', but it is '$VERSION_ID'"
    exit 1
fi

if [[ $PRETTY_NAME != $EXP_PRETTY_NAME ]]; then
    echo "FAIL: Expected PRETTY_NAME to be '$EXP_PRETTY_NAME', but it is '$PRETTY_NAME'"
    exit 1
fi

if [[ $ANSI_COLOR != $EXP_ANSI_COLOR ]]; then
    echo "FAIL: Expected ANSI_COLOR to be '$EXP_ANSI_COLOR', but it is '$ANSI_COLOR'"
    exit 1
fi

if [[ $CPE_NAME != $EXP_CPE_NAME ]]; then
    echo "FAIL: Expected CPE_NAME to be '$EXP_CPE_NAME', but it is '$CPE_NAME'"
    exit 1
fi

if [[ $HOME_URL != $EXP_HOME_URL ]]; then
    echo "FAIL: Expected HOME_URL to be '$EXP_HOME_URL', but it is '$HOME_URL'"
    exit 1
fi

if [[ $BUG_REPORT_URL != $EXP_BUG_REPORT_URL ]]; then
    echo "FAIL: Expected BUG_REPORT_URL to be '$EXP_BUG_REPORT_URL', but it is '$BUG_REPORT_URL'"
    exit 1
fi

if [[ $REDHAT_BUGZILLA_PRODUCT != $EXP_REDHAT_BUGZILLA_PRODUCT ]]; then
    echo "FAIL: Expected REDHAT_BUGZILLA_PRODUCT to be '$EXP_REDHAT_BUGZILLA_PRODUCT', but it is '$REDHAT_BUGZILLA_PRODUCT'"
    exit 1
fi

if [[ $REDHAT_BUGZILLA_PRODUCT_VERSION != $EXP_REDHAT_BUGZILLA_PRODUCT_VERSION ]];  then
    echo "FAIL: Expected REDHAT_BUGZILLA_PRODUCT_VERSION to be '$EXP_REDHAT_BUGZILLA_PRODUCT_VERSION', but it is '$REDHAT_BUGZILLA_PRODUCT_VERSION'"
    exit 1
fi

if [[ $REDHAT_SUPPORT_PRODUCT != $EXP_REDHAT_SUPPORT_PRODUCT ]];  then
    echo "FAIL: Expected REDHAT_SUPPORT_PRODUCT to be '$EXP_REDHAT_SUPPORT_PRODUCT', but it is '$REDHAT_SUPPORT_PRODUCT'"
    exit 1
fi

if [[ $REDHAT_SUPPORT_PRODUCT_VERSION != $EXP_REDHAT_SUPPORT_PRODUCT_VERSION ]];  then
    echo "FAIL: Expected REDHAT_SUPPORT_PRODUCT_VERSION to be '$EXP_REDHAT_SUPPORT_PRODUCT_VERSION', but it is '$REDHAT_SUPPORT_PRODUCT_VERSION'"
    exit 1
fi

if [[ $PRIVACY_POLICY_URL != $EXP_PRIVACY_POLICY_URL ]];  then
    echo "FAIL: Expected PRIVACY_POLICY_URL to be '$EXP_PRIVACY_POLICY_URL', but it is '$PRIVACY_POLICY_URL'"
    exit 1
fi

