FROM node:20-alpine AS base
RUN apk update
RUN apk upgrade --no-cache
RUN apk add --no-cache libc6-compat

FROM base AS build
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

FROM base AS web
COPY --from=build /app/node_modules /app/node_modules
COPY --from=build /app/package.json /app/package.json
COPY --from=build /app/build /app/build
WORKDIR /app

EXPOSE 3000
CMD [ "node", "build",  "--host", "0.0.0.0", "--port", "3000" ]