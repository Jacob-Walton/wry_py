FROM quay.io/pypa/manylinux_2_34_x86_64:latest

# Install pkg-config and GLib development headers so pkg-config can find glib-2.0.pc
RUN if command -v dnf >/dev/null 2>&1; then \
      dnf -y install pkgconfig glib2-devel && dnf clean all; \
    elif command -v yum >/dev/null 2>&1; then \
      yum -y install pkgconfig glib2-devel && yum clean all; \
    else \
      echo "No suitable package manager found" && exit 1; \
    fi

ENV PKG_CONFIG_PATH=/usr/lib64/pkgconfig:/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
