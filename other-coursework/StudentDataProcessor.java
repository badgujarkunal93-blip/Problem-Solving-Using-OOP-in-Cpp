import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/**
 * Assignment 2 - Multithreaded AI Data Processing System
 *
 * Simulates preprocessing 10,000 student records for an AI/ML pipeline.
 * It compares one worker processing every record with four workers processing
 * equal, non-overlapping portions of the same data set.
 */
public class StudentDataProcessor {
    private static final int RECORD_COUNT = 10_000;
    private static final int THREAD_COUNT = 4;

    private record StudentRecord(int id, int attendance, int testScore, int projects) { }
    private record WorkerResult(String workerName, int fromId, int toId, int count,
                                double featureTotal, long checksum) { }

    public static void main(String[] args) throws Exception {
        List<StudentRecord> records = createDataSet(RECORD_COUNT);

        System.out.println("============================================================");
        System.out.println("MULTITHREADED AI DATA PROCESSING SYSTEM");
        System.out.println("Dataset: " + records.size() + " student records");
        System.out.println("Task: feature extraction, validation, and checksum generation");
        System.out.println("============================================================\n");

        // Warm up the JVM so startup/JIT compilation has less influence on timing.
        processRange(records, 0, Math.min(200, records.size()), "Warm-up");

        System.out.println("1. SINGLE-THREADED EXECUTION");
        long singleStart = System.nanoTime();
        WorkerResult single = processRange(records, 0, records.size(), "Main thread");
        double singleMs = elapsedMilliseconds(singleStart);
        System.out.printf("   Main thread completed records %d-%d (%d records)%n",
                single.fromId(), single.toId(), single.count());
        System.out.printf("   Execution time: %.3f ms%n%n", singleMs);

        System.out.println("2. MULTITHREADED EXECUTION (" + THREAD_COUNT + " threads)");
        System.out.println("   Workload division:");
        int chunkSize = (records.size() + THREAD_COUNT - 1) / THREAD_COUNT;
        for (int i = 0; i < THREAD_COUNT; i++) {
            int start = i * chunkSize;
            int end = Math.min(start + chunkSize, records.size());
            if (start < end) {
                System.out.printf("   Worker-%d: record IDs %d-%d (%d records)%n",
                        i + 1, start + 1, end, end - start);
            }
        }

        long multiStart = System.nanoTime();
        ExecutorService pool = Executors.newFixedThreadPool(THREAD_COUNT);
        List<Future<WorkerResult>> futures = new ArrayList<>();
        for (int i = 0; i < THREAD_COUNT; i++) {
            int start = i * chunkSize;
            int end = Math.min(start + chunkSize, records.size());
            if (start >= end) break;
            int workerNumber = i + 1;
            futures.add(pool.submit(new Callable<>() {
                @Override
                public WorkerResult call() {
                    return processRange(records, start, end, "Worker-" + workerNumber);
                }
            }));
        }

        double multiFeatureTotal = 0.0;
        long multiChecksum = 0L;
        for (Future<WorkerResult> future : futures) {
            WorkerResult result = future.get();
            multiFeatureTotal += result.featureTotal();
            multiChecksum += result.checksum();
            System.out.printf("   %s completed records %d-%d (%d records)%n",
                    result.workerName(), result.fromId(), result.toId(), result.count());
        }
        pool.shutdown();
        double multiMs = elapsedMilliseconds(multiStart);

        boolean correct = Math.abs(single.featureTotal() - multiFeatureTotal) < 0.000001
                && single.checksum() == multiChecksum;
        double speedup = singleMs / multiMs;
        double improvement = (1.0 - multiMs / singleMs) * 100.0;

        System.out.printf("   Execution time: %.3f ms%n%n", multiMs);
        System.out.println("3. RESULT CHECK AND COMPARISON");
        System.out.println("   Equal results from both methods: " + (correct ? "PASS" : "FAIL"));
        System.out.printf("   Single-thread time: %.3f ms%n", singleMs);
        System.out.printf("   Multi-thread time : %.3f ms%n", multiMs);
        System.out.printf("   Speed-up          : %.2fx%n", speedup);
        System.out.printf("   Time change       : %.2f%%%n", improvement);
        System.out.println("\nNote: Results vary by CPU core count, system load, and JVM scheduling.");
    }

    private static List<StudentRecord> createDataSet(int count) {
        List<StudentRecord> records = new ArrayList<>(count);
        for (int i = 1; i <= count; i++) {
            records.add(new StudentRecord(i, 60 + (i * 7) % 41, 35 + (i * 13) % 66, (i * 3) % 6));
        }
        return records;
    }

    private static WorkerResult processRange(List<StudentRecord> records, int start, int end,
                                             String workerName) {
        double totalFeature = 0.0;
        long checksum = 0L;
        for (int i = start; i < end; i++) {
            StudentRecord record = records.get(i);
            // Normalised feature used by a hypothetical student-performance model.
            double feature = record.attendance() * 0.35 + record.testScore() * 0.50
                    + record.projects() * 3.0;
            totalFeature += feature;
            checksum += computeFingerprint(record.id(), record.attendance(), record.testScore());
        }
        return new WorkerResult(workerName, start + 1, end, end - start, totalFeature, checksum);
    }

    // CPU-intensive transformation stands in for realistic feature engineering.
    private static long computeFingerprint(int id, int attendance, int score) {
        long value = ((long) id << 32) ^ ((long) attendance << 16) ^ score;
        for (int i = 0; i < 6_000; i++) {
            value ^= value << 13;
            value ^= value >>> 7;
            value ^= value << 17;
        }
        return value;
    }

    private static double elapsedMilliseconds(long startNanos) {
        return (System.nanoTime() - startNanos) / 1_000_000.0;
    }
}
