# Resumen de Papers

Colección de resúmenes en español de papers sobre machine unlearning, sesgo en LLMs, interpretabilidad mecanística y alineamiento.

Este repositorio está configurado como un sitio Jekyll. El índice completo está en [`index.md`](index.md), que sirve como página de inicio del sitio.

---

## Ejecutar el sitio localmente

**1. Instalar Ruby + Bundler** (WSL/Ubuntu):
```bash
sudo apt update && sudo apt install ruby-full build-essential zlib1g-dev
gem install bundler
```

**2. Instalar dependencias:**
```bash
bundle install
```

**3. Iniciar el servidor:**
```bash
bundle exec jekyll serve
```

Abrir `http://localhost:4000` en el navegador. El sitio se recarga automáticamente al modificar archivos.

---

## Publicar en GitHub Pages

1. Subir el repositorio a GitHub.
2. Ir a **Settings → Pages → Source**, seleccionar la rama (`main`) y la carpeta raíz (`/`).
3. GitHub Actions construirá el sitio automáticamente.

> Si el repositorio está en `username.github.io/nombre-repo` (no en la raíz), ajustar en `_config.yml`:
> ```yaml
> baseurl: "/nombre-repo"
> ```