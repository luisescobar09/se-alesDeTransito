import web

urls = (
    "/","senales.index.Index"
)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()