from pythonforandroid.recipe import Recipe

class LibffiRecipe(Recipe):
    """
    Stub libffi recipe for CI:
    - Không chạy autogen.sh
    - Không chạy configure/make
    - Không build gì hết
    - Giả vờ như libffi đã có sẵn
    """
    name = "libffi"
    version = "ci-prebuilt-skip"
    url = None  # không download source

    def should_build(self, arch):
        # nói với p4a rằng: không cần build lại nữa
        return False

    def build_arch(self, arch):
        # cố ý không làm gì
        print("Using stubbed libffi on CI, skipping build.")
        return
