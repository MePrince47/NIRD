# Déploiement Docker minimal pour VPS

Ce petit guide montre comment déployer ce projet Django sur un VPS en utilisant Docker Compose et SQLite en volume persistant.

Prérequis sur le VPS:
- Docker et docker-compose installés
- Accès SSH

Étapes rapides:

1. Copier le dépôt sur le VPS (git clone / pull) dans `/srv/nird` ou un dossier de votre choix.
2. Créer un fichier `.env` à partir de `.env.example` et mettre `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` (ex: `example.com`) et garder `SQLITE_PATH=/data/db.sqlite3`.
	- Pour tester en local : mettez `HOST_PORT=8080` et dans `DJANGO_ALLOWED_HOSTS` incluez `localhost,127.0.0.1`.
	- Sur le VPS : mettez `HOST_PORT=80` et `DJANGO_ALLOWED_HOSTS=your.domain.com` (ou `your.domain.com,localhost,127.0.0.1` si vous voulez toujours accéder localement depuis le serveur).
3. Lancer la construction et le démarrage:

```bash
cd /srv/nird
docker compose up -d --build
```

Ce que fait la stack:
- Le service `web` construit une image Python, installe les dépendances, applique les migrations et collecte les fichiers statiques.
- Les volumes nommés `db_data` et `static_volume` garantissent la persistance de la base SQLite et des fichiers statiques.
- `nginx` sert les fichiers statiques et reverse-proxie vers gunicorn sur le service `web`.

Notes:
- Assurez-vous que le port 80 est ouvert sur le VPS.
 - Si vous testez localement, ouvrez `http://localhost:8080` (ou changez `HOST_PORT` dans `.env`). Sur le VPS mettez `HOST_PORT=80` pour exposer le service sur le port 80.
 - Si vous testez localement, ouvrez `http://localhost:8080` (ou changez `HOST_PORT` dans `.env`). Sur le VPS nous recommandons d'utiliser un reverse-proxy (Nginx ou Caddy) pour servir `nird-nta-techware.com` et reverse-proxier vers le service web exposé sur le port **8001**.

Configuration recommandée pour le VPS
1) DNS
	 - Créez un enregistrement A pour `nird-nta-techware.com` pointant vers l'IP de votre VPS.

2) Démarrer uniquement le service web (sans le conteneur Nginx local du repo)
	 - Sur le VPS, utilisez le nouveau fichier `docker-compose.prod.yml` qui expose Gunicorn sur le port `8001` :

```bash
# (sur le VPS)
cp .env .env.bak
# modifier .env : DJANGO_ALLOWED_HOSTS=nird-nta-techware.com
docker compose -f docker-compose.prod.yml up -d --build
```

3) Reverse-proxy (choisissez l'un des deux suivant ce que vous utilisez sur le VPS)

	A) Si vous utilisez system Nginx (fichier `/etc/nginx/sites-available/nird`)

```nginx
server {
		listen 80;
		server_name nird-nta-techware.com;

		location /static/ {
				# si vous montez staticfiles sur /srv/nird/staticfiles
				alias /srv/nird/staticfiles/;
		}

		location / {
				proxy_pass http://127.0.0.1:8001;
				proxy_set_header Host $host;
				proxy_set_header X-Real-IP $remote_addr;
				proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
				proxy_set_header X-Forwarded-Proto $scheme;
		}
}
```

	- Après création :

```bash
sudo ln -s /etc/nginx/sites-available/nird /etc/nginx/sites-enabled/nird
sudo nginx -t
sudo systemctl reload nginx
```

	B) Si votre VPS utilise Caddy (comme sur l'exemple que vous avez montré), ajoutez un bloc à votre `Caddyfile` :

```
nird-nta-techware.com {
		reverse_proxy 127.0.0.1:8001
		encode gzip
		log {
				output file /data/caddy/nird_access.log
		}
}
```

	- Puis redémarrez Caddy (si vous l'exécutez en Docker compose, redémarrez le conteneur `caddy_global`) :

```bash
docker compose restart caddy
# ou si caddy est systemd: sudo systemctl restart caddy
```

4) Tests
	- Vérifiez que `docker compose -f docker-compose.prod.yml ps` montre `nird_web` up and listening.
	- `curl -I http://127.0.0.1:8001` sur le VPS doit renvoyer un `200` si Gunicorn répond.
	- Depuis l'extérieur, `curl -I http://nird-nta-techware.com` doit renvoyer la même réponse via le reverse-proxy.

Remarques de sécurité
	- En production, utilisez HTTPS (Let's Encrypt). Caddy gère souvent automatiquement TLS. Pour Nginx, utilisez Certbot/Let's Encrypt et redirigez HTTP→HTTPS.

- Pour voir les logs: `docker compose logs -f`.
- Pour exécuter une commande Django:

```bash
docker compose run --rm web python manage.py createsuperuser
```
