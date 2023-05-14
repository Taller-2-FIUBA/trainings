"""Application configuration."""
from environ import config, var, group


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
        create_structures = var(False, converter=bool)

    @config
    class AUTH:
        """Authentication service configuration."""

        host = var("auth-service.fiufit.svc.cluster.local:8002")

    @config(prefix="FIREBASE")
    class Firebase:
        type: str = var("service_account")
        project_id: str = var("taller2-fiufit")
        private_key_id: str = var("404e45eb1856c2152c53e2a805e59b0b186ab956")
        private_key: str = var("https://tenor.com/bhDEJ.gif")
        client_email: str = var(
            "firebase-adminsdk-zwduu@taller2-fiufit.iam.gserviceaccount.com"
        )
        client_id: str = var("117815040269453856692")

    db = group(DB)  # type: ignore
    auth = group(AUTH)  # type: ignore
    firebase = group(Firebase)
