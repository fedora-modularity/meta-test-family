from moduleframework import dockerlinter, module_framework


class DockerInstructionsTests(module_framework.AvocadoTest):
    """
    :avocado: enable
    :avocado: tags=sanity,rhel,fedora,docker,docker_instruction_test,static

    """

    dp = None
    FROM = "https://docs.docker.com/engine/reference/builder/#from"
    def setUp(self):
        # it is not intended just for docker, but just docker packages are
        # actually properly signed
        self.dp = dockerlinter.DockerfileLinter()
        if self.dp.dockerfile is None:
            self.cancel("Dockerfile was not found")

    def test_from_is_first_directive(self):
        self.assertTrue(self.dp.check_from_is_first(),
                        msg="FROM instruction is not first.\nMore info: %s" % self.FROM)

    def test_from_directive_is_valid(self):
        reg_exp = '^[a-z0-9.]+(\/[a-z0-9\D.]+)+$'
        self.assertTrue(self.dp.check_from_directive_is_valid(),
                        msg="FROM instruction (%s) is not valid. We use reg %s."
                            "\nMore info: %s" % (self.dp.get_from_instruction(), reg_exp, self.FROM))

    def test_chained_run_dnf_commands(self):
        self.assertTrue(self.dp.check_chained_run_dnf_commands(), msg="dnf/yum commands are not chained.\n\tMore info: https://github.com/projectatomic/container-best-practices/blob/master/creating/creating_index.adoc#clearing-package-cache-and-squashing")

    def test_chained_run_rest_commands(self):
        self.assertTrue(self.dp.check_chained_run_rest_commands(), msg="RUN instructions are not chained.\n\tMore info: https://github.com/projectatomic/container-best-practices/blob/master/creating/creating_index.adoc#chaining-commands")

    def test_copy_files_exist(self):
        self.assertTrue(self.dp.check_copy_files_exist(), msg="Some files in the COPY or ADD instruction do not exist.")

    def test_helpmd_is_present(self):
        self.assert_to_warn(self.assertTrue, self.dp.check_helpmd_is_present(), msg="Help file is not present for this container.")


class DockerLabelsTests(DockerInstructionsTests):
    """
    :avocado: enable
    :avocado: tags=sanity,docker,docker_labels_test

    """

    def _test_for_env_and_label(self, docker_env, docker_label, env=True):
        label_found = True
        if env:
            label = self.dp.get_docker_specific_env(docker_env)
        else:
            label = self.dp.get_specific_label(docker_env)
        if not label:
            label_found = self.dp.get_specific_label(docker_label)
        return label_found

    def _get_msg(self, label, reference=None):
        msg = label + " is missing in Dockerfile."
        if reference:
            msg = msg + '\n\tMore info: ' + reference
        return msg

    def test_architecture_label_exists(self):
        """
        :avocado: tags=rhel,fedora
        """
        self.assertTrue(self.dp.get_specific_label("architecture"),
                        msg=self._get_msg("architecture label",
                                          reference='https://docs.docker.com/engine/reference/builder/#from'))

    def test_name_in_env_and_label_exists(self):
        """
        :avocado: tags=fedora
        """
        self.assertTrue(self.dp.get_docker_specific_env("NAME="), msg=self._get_msg("Environment variable NAME"))
        self.assertTrue(self.dp.get_specific_label("name"),
                        msg=self._get_msg("Label name",
                                          reference='https://fedoraproject.org/wiki/Container:Guidelines#LABELS'))

    def test_maintainer_label_exists(self):
        """
        :avocado: tags=fedora
        """
        self.assertTrue(self.dp.get_specific_label("maintainer"),
                        msg=self._get_msg("Label maintainer",
                                          reference='https://fedoraproject.org/wiki/Container:Guidelines#LABELS'))

    def test_release_label_exists(self):
        """
        :avocado: tags=fedora
        """
        self.assertTrue(self.dp.get_specific_label("release"),
                        msg=self._get_msg("Label release",
                                          reference='https://fedoraproject.org/wiki/Container:Guidelines#LABELS'))

    def test_version_label_exists(self):
        """
        :avocado: tags=rhel,fedora
        """
        self.assertTrue(self.dp.get_specific_label("version"),
                        msg=self._get_msg("Label version",
                                          reference='https://fedoraproject.org/wiki/Container:Guidelines#LABELS'))

    def test_com_redhat_component_label_exists(self):
        """
        :avocado: tags=rhel,fedora
        """
        self.assertTrue(self.dp.get_specific_label("com.redhat.component"),
                        msg=self._get_msg("Label com.redhat.component",
                                          reference='https://fedoraproject.org/wiki/Container:Guidelines#LABELS'))

    def test_summary_label_exists(self):
        """
        :avocado: tags=rhel,fedora
        """
        self.assertTrue(self.dp.get_specific_label("summary"),
                        msg=self._get_msg("Label summary",
                                          reference='https://fedoraproject.org/wiki/Container:Guidelines#LABELS'))

    def test_run_or_usage_label_exists(self):
        """
        :avocado: tags=fedora
        """
        self.assertTrue(self._test_for_env_and_label("run", "usage", env=False),
                        msg=self._get_msg("Label run or usage",
                                          reference='https://fedoraproject.org/wiki/Container:Guidelines#LABELS'))


