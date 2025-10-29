from pythonforandroid.recipe import Recipe


class LibffiRecipe(Recipe):
    name = "libffi"
    version = "fake-prebuilt-for-ci"
    url = None  # we are not downloading source

    def should_build(self, arch):
        # Pretend it's already built to skip compile steps
        return False

    def build_arch(self, arch):
        # Do nothing: skip ./autogen.sh, ./configure, make, etc.
        print("Using stub libffi for CI (no build)")
        return
