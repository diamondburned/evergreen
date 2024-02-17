import { promisify } from "util";
import fetch from "node-fetch";
import * as child_process from "child_process";
import * as path from "path";
import * as fs from "fs/promises";
import * as os from "os";

const BACKEND_PORT = 5766;

async function generateForDir(tmpDir) {
  console.debug("Fetching openapi.json...");
  let response;
  while (true) {
    try {
      response = await fetch(`http://localhost:${BACKEND_PORT}/openapi.json`);
      break;
    } catch (e) {
      await sleep(200);
    }
  }

  if (!response.ok) {
    throw new Error(`Failed to fetch openapi.json: ${response.statusText}`);
  }

  const openapiData = await response.text();
  const openapiPath = path.join(tmpDir, "openapi.json");
  await fs.writeFile(openapiPath, openapiData);
  console.debug(`Fetched openapi.json to ${openapiPath}`);

  await oazapfts(openapiPath, `./frontend/lib/api/openapi.ts`, ["optimistic", "useEnumType"]);
  console.debug(`Generated TypeScript client to ./frontend/lib/api/openapi.ts`);
}

async function oazapfts(spec, filename, flags = []) {
  flags = flags.map((flag) => `--${flag}`);
  const args = ["oazapfts", spec, filename, ...flags];
  await execFile(args[0], args.slice(1));
}

const execFile = promisify(child_process.execFile);

async function startBackend() {
  const abortController = new AbortController();
  const argv = ["python3", "-m", "backend", "--port", `${BACKEND_PORT}`, "--database", ":memory:"];
  let cmdPromise = execFile(argv[0], argv.slice(1), {
    signal: abortController.signal,
    killSignal: "SIGINT",
  });
  cmdPromise = cmdPromise.catch((err) => {
    if (!abortController.signal.aborted) {
      throw err;
    }
  });
  return async () => {
    abortController.abort();
    await cmdPromise;
  };
}

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function generate() {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "openapi-"));
  const stopBackend = await startBackend();
  try {
    await generateForDir(tempDir);
  } finally {
    await stopBackend();
    await fs.rm(tempDir, { recursive: true });
  }
}

// https://stackoverflow.com/a/72206110
const isMainModule = import.meta.url.endsWith(process.argv[1]);
if (isMainModule) {
  generate().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}
