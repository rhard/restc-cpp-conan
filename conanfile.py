from conans import ConanFile, CMake, tools
import shutil


class RestccppConan(ConanFile):
    name = "restc_cpp"
    version = "0.9.2"
    license = "MIT License"
    url = "https://github.com/rhard/restc-cpp"
    description = "REST API c++ library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "tls": [
        True, False], "zlib": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "tls=True", "zlib=True", "fPIC=True"
    generators = "cmake"

    def source(self):
        tools.rmdir("restc-cpp")
        self.run("git clone https://github.com/rhard/restc-cpp")
        self.run("cd restc-cpp && git checkout 0a6f5626e054274e43e184ad9ce41f0544684243")
        tools.replace_in_file("restc-cpp/CMakeLists.txt", "include(cmake_scripts/external-projects.cmake)","#include(cmake_scripts/external-projects.cmake)")
        tools.replace_in_file("restc-cpp/CMakeLists.txt", "if (EXISTS ${Boost_INCLUDE_DIRS}/boost/type_index.hpp)","if (1)")
        tools.replace_in_file("restc-cpp/CMakeLists.txt", "add_dependencies(${PROJECT_NAME} externalRapidJson)","#add_dependencies(${PROJECT_NAME} externalRapidJson)")

    def requirements(self):
        self.requires("rapidjson/1.1.0@bincrafters/stable")
        self.requires("boost/1.67.0@conan/stable")
        #self.requires("boost_system/1.66.0@bincrafters/stable")
        #self.requires("boost_program_options/1.66.0@bincrafters/stable")
        #self.requires("boost_filesystem/1.66.0@bincrafters/stable")
        #self.requires("boost_date_time/1.66.0@bincrafters/stable")
        #self.requires("boost_context/1.66.0@bincrafters/stable")
        #self.requires("boost_coroutine/1.66.0@bincrafters/stable")
        #self.requires("boost_chrono/1.66.0@bincrafters/stable")
        #self.requires("boost_log/1.66.0@bincrafters/stable")
        #self.requires("boost_uuid/1.66.0@bincrafters/stable")
        #self.requires("boost_type_index/1.66.0@bincrafters/stable")
        if self.options.tls:
            self.requires("OpenSSL/1.1.0g@conan/stable")
        if self.options.zlib:
            self.requires("zlib/1.2.11@conan/stable")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["INSTALL_RAPIDJSON_HEADERS"] = "OFF"
        cmake.definitions["WITH_APIDOC"] = "OFF"
        cmake.definitions["RESTC_CPP_WITH_EXAMPLES"] = "OFF"
        cmake.definitions["RESTC_CPP_WITH_UNIT_TESTS"] = "OFF"
        cmake.definitions["RESTC_CPP_AUTORUN_UNIT_TESTS"] = "OFF"
        cmake.definitions["RESTC_CPP_WITH_FUNCTIONALT_TESTS"] = "OFF"
        if self.options.tls:
            cmake.definitions["RESTC_CPP_WITH_TLS"] = "ON"
        else:
            cmake.definitions["RESTC_CPP_WITH_TLS"] = "OFF"
        if self.options.zlib:
            cmake.definitions["RESTC_CPP_WITH_ZLIB"] = "ON"
        else:
            cmake.definitions["RESTC_CPP_WITH_ZLIB"] = "OFF"
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.configure(source_folder="restc-cpp")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="restc-cpp/include")
        self.copy("*.hpp", dst="include", src="restc-cpp/include")
        self.copy("*.h", dst="include/restc-cpp", src="generated-include/restc-cpp")
        self.copy("*.h", dst="include/restc-cpp", src="include-exports/restc-cpp")
        self.copy("*restc-cpp.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["restc-cpp"]
