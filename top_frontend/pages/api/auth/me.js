// api/auth/me.ts
import { handleProfile } from "@auth0/nextjs-auth0";

const profileHandler = async (req, res) => {
  try {
    await handleProfile(req, res);
  } catch (error) {
    res.status(error.status || 400).end(error.message);
  }
};

export default profileHandler;
