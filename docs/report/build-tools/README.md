# Building Instructions

1. From inside the `docs/report/build-tools` directory, run:
```sh
docker build --tag reportbuilder --file report-builder.Dockerfile .
```
2. Then, from inside the `docs/report/` directory, run:
```sh
docker run -it --rm --user `id -u` -v `pwd`:/report reportbuilder bash ./report/build-tools/compile-md.sh
```
3. Now look in `docs/report/output` for the generated files
