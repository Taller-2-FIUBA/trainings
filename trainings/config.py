"""Application configuration."""
from environ import bool_var, config, var, group


@config(prefix="TRAININGS")
class AppConfig:
    """Application configuration values from environment."""

    log_level = var("WARNING")
    prometheus_port = var(9001, converter=int)

    @config
    class DB:
        """Database configuration."""

        driver = var("postgresql")
        password = var("backend")
        user = var("backend")
        host = var("localhost")
        port = var(5432, converter=int)
        database = var("postgres")
        create_structures = bool_var(False)
        ssl = bool_var(True)

    @config
    class AUTH:
        """Authentication service configuration."""

        host = var("auth-service.fiufit.svc.cluster.local:8002")
        validate_credentials = bool_var(True)

    @config(prefix="FIREBASE")
    class Firebase:
        """Firebase configuration."""

        type: str = var("service_account")
        project_id: str = var("taller2-fiufit")
        private_key_id: str = var("404e45eb1856c2152c53e2a805e59b0b186ab956")
        private_key: str = var("https://tenor.com/bhDEJ.gif")
        client_email: str = var(
            "firebase-adminsdk-zwduu@taller2-fiufit.iam.gserviceaccount.com"
        )
        client_id: str = var("117815040269453856692")
        auth_uri: str = var("https://accounts.google.com/o/oauth2/auth")
        token_uri: str = var("https://oauth2.googleapis.com/token")
        auth_provider_x509_cert_url: str = var(
            "https://www.googleapis.com/oauth2/v1/certs"
        )
        client_x509_cert_url: str = var(
            "https://www.googleapis.com/robot/v1/metadata/x509/"
            "firebase-adminsdk-zwduu%40taller2-fiufit.iam.gserviceaccount.com"
        )
        storage_bucket: str = var("taller2-fiufit.appspot.com")

    @config(prefix="SENTRY")
    class Sentry:
        """Sentry configuration."""

        enabled = bool_var(False)
        dsn = var("https://token@sentry.ingest.localhost")

    db = group(DB)  # type: ignore
    auth = group(AUTH)  # type: ignore
    firebase = group(Firebase)
    sentry = group(Sentry)
