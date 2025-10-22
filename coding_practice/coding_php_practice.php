<?php
/*class InMemoryDB
{
    private array $db;

    public function __construct()
    {
        // create the "database" as an empty array
        $this->db = [];
    }

    public function set(string $key, mixed $value): void
    {
        $this->db[$key] = $value;
    }

    public function get(string $key): mixed
    {
        return $this->db[$key] ?? null;
    }
}

// --- usage ---
$db = new InMemoryDB();   // constructor creates db
$db->set("name", "Zahra");
echo $db->get("name");    // prints: Zahra */

$list=['zahra','shefa'];
function name($l){
foreach ($l as $e){
    echo $e;
}
}
name($list);
?>