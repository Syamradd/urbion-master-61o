# Render preflight repair

Production preflight exposed a real frontend asset routing failure. The repair adds a middleware-level allowlisted asset path guard so legacy wildcard routes cannot shadow championship JavaScript assets.
