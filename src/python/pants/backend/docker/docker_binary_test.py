# Copyright 2021 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from hashlib import sha256
from os import path

from pants.backend.docker.docker_binary import DockerBinary
from pants.engine.fs import Digest
from pants.engine.process import Process


def test_docker_binary_build_image():
    source_path = "src/test/repo"
    docker_path = "/bin/docker"
    dockerfile = path.join(source_path, "Dockerfile")
    docker = DockerBinary(docker_path)
    digest = Digest(sha256().hexdigest(), 123)
    tag = "test:latest"
    build_request = docker.build_image(tag, digest, source_path, dockerfile)

    assert build_request == Process(
        argv=(docker_path, "build", "-t", tag, "-f", dockerfile, source_path),
        input_digest=digest,
        description=f"Building docker image {tag}",
    )
