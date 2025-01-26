export function getClasses(): any {
    return {
        "warrior":"近卫",
        "caster":"术师",
        "medic":"医疗",
        "pioneer":"先锋",
        "sniper":"狙击",
        "special":"特种",
        "support":"辅助",
        "tank":"重装"
    }
}

export function getClassImage(className:string): string {
    return `/classes/${className.toUpperCase()}.png`
}
