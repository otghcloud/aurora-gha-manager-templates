<img src="https://otgh-static-assets.s3.otgh.cloud/branding/logos/otgh_cloud_2024.png" alt="OTGH Cloud" width="200px" />

# Aurora GHARM Templates

This repository contains the generated build templates for GitHub's hosted Actions Runner images, for use by our [GitHub Actions Runner Manager](https://github.com/otghcloud/aurora-gha-manager) project.

These are built using the scripts from the official [GitHub actions/runner-images repository](https://github.com/actions/runner-images); the resulting runners are 100% compatible with the official ones with unmodified contents - all changes are within the build/provisioning process itself.

## Usage

This repository is primarily intended to be consumed by our [GitHub Actions Runner Manager](https://github.com/otghcloud/aurora-gha-manager) project (an end to end building and JIT provisioning management platform for Proxmox), however it's relatively trivial to build the Packer templates yourself within a standard Proxmox environment. 

Documentation is in the works and will available in due course.

## Contributing

We'd love to have your input and value all contributions, large or small.

Please review [CONTRIBUTING.md](CONTRIBUTING.md) for additional information and required conventions.

## License

This repository uses the MIT license.

Please review [LICENSE.md](LICENSE.md) for more details.

## Security

Please review [SECURITY.md](SECURITY.md) for more details.