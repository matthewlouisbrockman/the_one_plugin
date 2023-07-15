import { getAccessToken, withApiAuthRequired } from "@auth0/nextjs-auth0";

const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:5000";

export default withApiAuthRequired(async function myApiRoute(req, res) {
  try {
    const { accessToken } = await getAccessToken(req, res);

    // Use the access token to call your API
    const result = await fetch(BASE_URL + "/management/jobs", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    // assuming the API response is JSON
    const data = await result.json();
    res.status(200).json(data);
  } catch (error) {
    console.error(error);
    res.status(error.status || 500).end(error.message);
  }
});
