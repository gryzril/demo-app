<template>
  <div class="min-h-screen grid place-items-center p-6">
    <div class="w-full max-w-md">
      <h1 class="text-2xl font-semibold mb-4">Login</h1>
      <Card>
        <template #content>
          <form @submit.prevent="onSubmit" class="space-y-4">
            <div>
              <label class="block text-sm mb-1">Email</label>
              <InputText v-model="email" type="email" placeholder="you@example.com" class="w-full" />
            </div>
            <div>
              <label class="block text-sm mb-1">Password</label>
              <Password v-model="password" :feedback="false" toggle-mask class="w-full" input-class="w-full" />
            </div>
            <Button type="submit" label="Sign in" class="w-full" :loading="loading" />
          </form>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "primevue/usetoast";
import Card from "primevue/card";
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import { login } from "@/api/client";

const router = useRouter();
const toast = useToast();

const email = ref("");
const password = ref("");
const loading = ref(false);

async function onSubmit() {
  if (!email.value || !password.value) {
    toast.add({ severity: "warn", summary: "Missing fields", detail: "Enter email and password" });
    return;
  }
  loading.value = true;
  try {
    const res = await login(email.value, password.value)
    localStorage.setItem("access_token", res.access_token);
    toast.add({ severity: "success", summary: "Signed in" });
    router.push("/dashboard");
  } catch (err: any) {
    toast.add({ severity: "error", summary: "Login failed", detail: err?.message ?? "Error" });
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.min-h-screen { min-height: 100vh; }
</style>
