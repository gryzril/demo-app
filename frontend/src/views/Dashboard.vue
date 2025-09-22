<template>
  <div class="p-6 space-y-4">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-semibold">Dashboard</h1>
      <div class="flex items-center gap-2">
        <Button label="New Task" icon="pi pi-plus" @click="openCreate()" />
        <Button label="Refresh" icon="pi pi-refresh" severity="secondary" @click="load()" :loading="loading" />
      </div>
    </div>

    <DataTable :value="tasks" data-key="id" :loading="loading" paginator :rows="10" responsive-layout="scroll">
      <Column field="title" header="Title" />
      <Column field="status" header="Status" />
      <Column field="due_date" header="Due">
        <template #body="{ data }">{{ fmtDate(data.due_date) }}</template>
      </Column>
      <Column header="Actions" style="width: 10rem">
        <template #body="{ data }">
          <Button icon="pi pi-trash" severity="danger" text rounded @click="remove(data.id)" />
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="showCreate" header="Create Task" modal :style="{ width: '32rem' }">
      <div class="space-y-4">
        <div>
          <label class="block text-sm mb-1">Title</label>
          <InputText v-model="form.title" class="w-full" />
        </div>
        <div>
          <label class="block text-sm mb-1">Description</label>
          <InputTextarea v-model="form.description" class="w-full" rows="3" />
        </div>
        <div>
          <label class="block text-sm mb-1">Status</label>
          <Dropdown v-model="form.status" :options="statuses" optionLabel="label" optionValue="value" class="w-full" />
        </div>
        <div>
          <label class="block text-sm mb-1">Due date</label>
          <Calendar v-model="form.due_date" showIcon class="w-full" />
        </div>
      </div>
      <template #footer>
        <Button label="Cancel" severity="secondary" @click="showCreate = false" />
        <Button label="Create" :loading="creating" @click="create()" />
      </template>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useToast } from "primevue/usetoast";
import Button from "primevue/button";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
//import InputTextarea from "primevue/inputtextarea";
import Dropdown from "primevue/dropdown";
import Calendar from "primevue/calendar";
// import { api } from "@/api/client";

type Task = {
  id: number;
  title: string;
  description?: string | null;
  status: "todo" | "doing" | "done";
  due_date?: string | null;
  created_at?: string;
  updated_at?: string;
};

const toast = useToast();
const tasks = ref<Task[]>([]);
const loading = ref(false);

const showCreate = ref(false);
const creating = ref(false);
const statuses = [
  { label: "Todo", value: "todo" },
  { label: "Doing", value: "doing" },
  { label: "Done", value: "done" },
];

const form = ref<{ title: string; description?: string; status: Task["status"]; due_date: Date | null }>({
  title: "",
  description: "",
  status: "todo",
  due_date: null,
});

function authHeaders() {
  const t = localStorage.getItem("access_token");
  return t ? { Authorization: `Bearer ${t}` } : {};
}

// async function load() {
//   loading.value = true;
//   try {
//     const data = await api<Task[]>("/tasks", { headers: { ...authHeaders() } });
//     tasks.value = data;
//   } catch (err: any) {
//     toast.add({ severity: "error", summary: "Load failed", detail: err?.message ?? "Error" });
//   } finally {
//     loading.value = false;
//   }
// }

function openCreate() {
  form.value = { title: "", description: "", status: "todo", due_date: null };
  showCreate.value = true;
}

// async function create() {
//   if (!form.value.title) {
//     toast.add({ severity: "warn", summary: "Title required" });
//     return;
//   }
//   creating.value = true;
//   const payload = {
//     title: form.value.title,
//     description: form.value.description || null,
//     status: form.value.status,
//     due_date: form.value.due_date ? form.value.due_date.toISOString() : null,
//     label_ids: [] as number[],
//   };
//   try {
//     const t = await api<Task>("/tasks", {
//       method: "POST",
//       headers: { ...authHeaders() },
//       body: JSON.stringify(payload),
//     });
//     tasks.value = [t, ...tasks.value]; // optimistic insert
//     showCreate.value = false;
//     toast.add({ severity: "success", summary: "Task created" });
//   } catch (err: any) {
//     toast.add({ severity: "error", summary: "Create failed", detail: err?.message ?? "Error" });
//   } finally {
//     creating.value = false;
//   }
// }

// async function remove(id: number) {
//   const prev = tasks.value.slice();
//   tasks.value = tasks.value.filter((x) => x.id !== id);
//   try {
//     await api<void>(`/tasks/${id}`, { method: "DELETE", headers: { ...authHeaders() } });
//     toast.add({ severity: "info", summary: "Task deleted" });
//   } catch (err: any) {
//     tasks.value = prev; // rollback
//     toast.add({ severity: "error", summary: "Delete failed", detail: err?.message ?? "Error" });
//   }
// }

function fmtDate(s?: string | null) {
  if (!s) return "";
  const d = new Date(s);
  return d.toLocaleDateString();
}

// onMounted(load);
</script>
