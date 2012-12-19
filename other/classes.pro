-injars classes.jar
-outjars classes_opt.jar

-libraryjars android.jar

-dontskipnonpubliclibraryclassmembers
-dontshrink
-optimizations method/inlining/*,code/merging,code/simplification/*
-optimizationpasses 9
-dontobfuscate
-dontpreverify
-verbose
-ignorewarnings


# Keep - Applications. Keep all application classes, along with their 'main'
# methods.
-keepclasseswithmembers public class * {
    public static void main(java.lang.String[]);
}

# Also keep - Enumerations. Keep the special static methods that are required in
# enumeration classes.
-keepclassmembers enum  * {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}

# Also keep - Database drivers. Keep all implementations of java.sql.Driver.
-keep class * extends java.sql.Driver

# Also keep - Swing UI L&F. Keep all extensions of javax.swing.plaf.ComponentUI,
# along with the special 'createUI' method.
-keep class * extends javax.swing.plaf.ComponentUI {
    public static javax.swing.plaf.ComponentUI createUI(javax.swing.JComponent);
}

# Keep names - Native method names. Keep all native class/method names.
-keepclasseswithmembers,allowshrinking class * {
    native <methods>;
}

# Remove debugging - Throwable_printStackTrace calls. Remove all invocations of
# Throwable.printStackTrace().
-assumenosideeffects public class java.lang.Throwable {
    public void printStackTrace();
}

# Remove debugging - Thread_dumpStack calls. Remove all invocations of
# Thread.dumpStack().
-assumenosideeffects public class java.lang.Thread {
    public static void dumpStack();
}

# Remove debugging - All logging API calls. Remove all invocations of the
# logging API whose return values are not used.
-assumenosideeffects public class java.util.logging.* {
    <methods>;
}

# Remove debugging - All Log4j API calls. Remove all invocations of the
# Log4j API whose return values are not used.
-assumenosideeffects public class org.apache.log4j.** {
    <methods>;
}
