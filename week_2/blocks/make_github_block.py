from prefect.filesystems import GitHub

github_block = GitHub(
    name="zoom-github",
    repository="https://github.com/andreishvaidyuk/de_zoomcamp/tree/main/week_2"
)
github_block.save("zoom-github", overwrite=True)