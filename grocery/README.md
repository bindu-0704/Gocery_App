# backend
``` cd backend ```
``` source myenv/bin/activate ```
``` python app.py ```

# celery
``` cd backend ```
``` source myenv/bin/activate ```
``` celery -A app.celery worker --loglevel=info -B```

# REDIS
``` redis-server```

# mailhog
``` cd backend ```
``` source myenv/bin/activate ```
```~/go/bin/MailHog```

# grocery

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
