# 🔍 Pickle序列化兼容性分析报告（不同操作系统间）

**分析场景**: `result_different_system` 目录结果


## 🚨 存在哈希值不一致的用例

### 📌 测试用例: container_dict
⚠️ **发现 2 个哈希组**

#### 组 #1
- 哈希: `76a763172fb8e65aca01ab99...`
- 包含 1 个环境:
  - Python 3.12.3 Protocol 1 linux

#### 组 #2
- 哈希: `9c90b93b9f9c18d6e2ae3f45...`
- 包含 1 个环境:
  - Python 3.12.4 Protocol 1 win32

### 📌 测试用例: special_pathlib
⚠️ **发现 2 个哈希组**

#### 组 #1
- 哈希: `bc0efc9159d65bc65fe84931...`
- 包含 1 个环境:
  - Python 3.12.3 Protocol 1 linux

#### 组 #2
- 哈希: `37e72339bb2f0c729da5bbc5...`
- 包含 1 个环境:
  - Python 3.12.4 Protocol 1 win32

## ✅ 哈希值一致的用例

### 📌 测试用例: primitive_int
🎯 统一哈希: `e915f694ae8f6861f8be3d44...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: primitive_string
🎯 统一哈希: `5843a7f04aa47437de68f154...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: primitive_float
🎯 统一哈希: `f90d214adb219a628422ceee...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: primitive_bool_true
🎯 统一哈希: `8252f6b37cd88a9afd6c793d...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: primitive_bool_false
🎯 统一哈希: `b5c02fe928cc341f80db9f9d...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: primitive_none
🎯 统一哈希: `8b1663da576e3578fd9e93e6...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: container_list
🎯 统一哈希: `b44616af1f96b9421d9496df...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: container_tuple
🎯 统一哈希: `527b4a72a3e3affb61667610...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: container_set
🎯 统一哈希: `65fadeb99af27cee26dec605...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: container_frozenset
🎯 统一哈希: `3d2f22db0032de68b0ce8aa9...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: container_deque
🎯 统一哈希: `fd6efdf7495f63d14bdf99cf...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: container_bytearray
🎯 统一哈希: `26963808c516219bbd255abf...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: container_memoryview
🎯 统一哈希: `ERROR::cannot pickle 'me...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux

### 📌 测试用例: container_nested
🎯 统一哈希: `aaf3074c2f462f1a32255e04...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: custom_simple
🎯 统一哈希: `216926d5998b11c02d7cd47f...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: custom_nested
🎯 统一哈希: `6fe07e1f6b8cd14cee36d882...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: custom_cyclic
🎯 统一哈希: `77f56d0a3112ac36e4a2f900...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: custom_slots
🎯 统一哈希: `ERROR::a class that defi...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: special_datetime
🎯 统一哈希: `190db49f339b84474edb8aa2...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: special_enum
🎯 统一哈希: `26eee1d390e87f1e22a4c3df...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: special_recursive_dict
🎯 统一哈希: `b3165ea6c2be18a978e52269...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32

### 📌 测试用例: special_nan_float
🎯 统一哈希: `2ff4d9bd70ae63ab256cfcb7...`

**包含环境:**
- Python 3.12.3 Protocol 1 linux
- Python 3.12.4 Protocol 1 win32