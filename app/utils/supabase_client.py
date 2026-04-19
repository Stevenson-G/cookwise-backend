from supabase import create_client
import uuid
import os

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)



def upload_image(file):
    try:
        file_ext = file.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_ext}"

        file_content = file.file.read()

        print("SUBIENDO A SUPABASE...")

        res = supabase.storage.from_("recipes-images").upload(
            file_name,
            file_content,
            {"content-type": file.content_type}
        )

        print("RESPUESTA SUPABASE:", res)

        public_url = supabase.storage.from_("recipes-images").get_public_url(file_name)

        print("URL GENERADA:", public_url)

        if isinstance(public_url, dict):
            return public_url.get("publicUrl")

        return public_url

    except Exception as e:
        print("ERROR REAL SUPABASE:", str(e))
        return None