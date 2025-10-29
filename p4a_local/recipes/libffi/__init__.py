from pythonforandroid.recipe import Recipe
from pythonforandroid.toolchain import current_directory
import shutil
import os
import subprocess


class LibffiRecipe(Recipe):
    name = "libffi"
    version = "3.4.4"
    url = "https://github.com/libffi/libffi/releases/download/v{version}/libffi-{version}.tar.gz"
    built_libraries = {"libffi.so": "build/.libs"}

    def build_arch(self, arch):
        env = self.get_recipe_env(arch)
        build_dir = self.get_build_dir(arch.arch)
        with current_directory(build_dir):
            configure_cmd = [
                "./configure",
                f"--host={arch.command_prefix}",
                f"--build={arch.host_platform}",
                "--disable-static",
                "--enable-shared",
                "--with-pic",
            ]
            subprocess.check_call(configure_cmd, env=env)
            subprocess.check_call(["make", "-j4"], env=env)

    def install_arch(self, arch):
        env = self.get_recipe_env(arch)
        build_dir = self.get_build_dir(arch.arch)
        with current_directory(build_dir):
            lib_dir = os.path.join(self.ctx.get_libs_dir(arch.arch))
            os.makedirs(lib_dir, exist_ok=True)
            shutil.copy2(os.path.join("build", ".libs", "libffi.so"), lib_dir)


recipe = LibffiRecipe()
