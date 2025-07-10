## 📘 SQLite Schema Documentation – *djvu_sqlite.db*

### 📌 Tables Overview

#### 1. **`forms`**
Stores metadata about dictionary entries or image forms.

| Column        | Type    | Constraints                                   |
|---------------|---------|-----------------------------------------------|
| `id`          | INTEGER | Primary Key, Auto-increment, Unique           |
| `position`    | INTEGER | Unique, Not Null                              |
| `entry_name`  | STRING  | Not Null                                      |
| `type`        | INTEGER | Not Null                                      |
| `path_to_dump`| STRING  | —                                             |

---

#### 2. **`sqlite_sequence`**
Used by SQLite internally to track `AUTOINCREMENT` fields.

| Column | Type   |
|--------|--------|
| `name` | TEXT   |
| `seq`  | INTEGER|

---

#### 3. **`sjbz_info`**
Describes metadata for scanned or processed documents.

| Column    | Type    | Constraints                                  |
|-----------|---------|----------------------------------------------|
| `form_id` | INTEGER | Not Null, Unique, FK → `forms(id)`           |
| `djbz_id` | INTEGER | FK → `forms(id)`                              |
| `width`   | INTEGER | Not Null                                     |
| `height`  | INTEGER | Not Null                                     |
| `dpi`     | INTEGER | Not Null                                     |
| `version` | INTEGER | Not Null                                     |

---

#### 4. **`letters`**
Captures bounding box and image data for recognized letters.

| Column         | Type    | Constraints                                 |
|----------------|---------|---------------------------------------------|
| `id`           | INTEGER | Primary Key, Auto-increment, Unique, Not Null |
| `form_id`      | INTEGER | Not Null, FK → `forms(id)`                  |
| `local_id`     | INTEGER | —                                           |
| `x`            | INTEGER | —                                           |
| `y`            | INTEGER | —                                           |
| `width`        | INTEGER | Not Null                                    |
| `height`       | INTEGER | Not Null                                    |
| `in_image`     | INTEGER | Not Null                                    |
| `in_library`   | INTEGER | Not Null                                    |
| `is_non_symbol`| INTEGER | Not Null                                    |
| `reference_id` | INTEGER | FK → `letters(id)`                          |
| `is_refinement`| INTEGER | —                                           |
| `filename`     | STRING  | —                                           |

**Index**:  
- `index_letters` on `(form_id, local_id)`